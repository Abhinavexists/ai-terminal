import os
import re
from executor import CommandResponse, run_command
from agent import commands
from safety import CommandSafety, RiskLevel
from commands import shell_commands
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from prompt_toolkit.completion import FuzzyWordCompleter
from rich import print

HISTORY_FILE = os.path.expanduser("~/.terminal_history")

def load_previous_commands():
    if not os.path.exists(HISTORY_FILE):
        return []
    with open(HISTORY_FILE, "r") as file:
        return list(set([line.strip() for line in file if line.strip()]))

def save_command(cmd: str):
    with open(HISTORY_FILE, "a") as file:
        file.write(cmd + "\n")

PLACEHOLDER_PATTERNS = [                                         # regex patterns for placeholders
    r"<[^>]+>",                                                  # <placeholder>
    r"\b(old|new)[-_]?(file|filename|path|dir)\b",               # old_file, new_filename
    r"\b(source|destination)[-_ ]?(file|directory|dir|path)\b",  # source_file, destination_dir
    r"\bYOUR[_-]?(FILE|PATH|DIR|BRANCH|REPO)\b",                 # YOUR_FILE, YOUR_PATH
]

def placeholders(cmd: str) -> bool:
    for pat in PLACEHOLDER_PATTERNS:
        if re.search(pat, cmd, flags=re.IGNORECASE):
            return True
    return False

def shell_command(user_input: str) -> bool:
    """Check if user input looks like a valid shell command."""
    input_lower = user_input.lower().strip()
    words = input_lower.split()
    
    if not words:
        return False
    
    first_word = words[0]
    
    all_commands = []
    for category, commands in shell_commands.items():
        if isinstance(commands, list):
            all_commands.extend(commands)
        elif isinstance(commands, dict):
            for os_commands in commands.values():
                all_commands.extend(os_commands)
    
    if first_word in all_commands:
        return True
    
    if re.match(r'^[./]', first_word) or re.search(r'[|&;<>]', user_input):
        return True
    
    return False

def edit_command(suggested: str) -> str:
    print(f"[cyan]Current command:[/cyan] {suggested}")
    print("[magenta]Edit the command (press Enter to keep as is):[/magenta]")
    edited = input("> ").strip()
    return edited if edited else suggested

def check_command_safety(cmd: str) -> bool:
    """Check if a command is safe to execute and get user confirmation if needed."""
    safety_result = CommandSafety().analyse_command(cmd)
    
    if safety_result.blocked and safety_result.risk_level == RiskLevel.CRITICAL:
        print(f"[red]{safety_result.warning[0]}[/red]")
        if safety_result.suggestions:
            print(f"[yellow]Suggestions:[/yellow]")
            for suggestion in safety_result.suggestions:
                print(f"  • {suggestion}")
        return False
    
    if safety_result.warning:
        print(f"\n[bold yellow]Safety Warning:[/bold yellow]")
        for warning in safety_result.warning:
            print(f"[yellow]{warning}[/yellow]")
        
        if safety_result.suggestions:
            print(f"[cyan]Suggestions:[/cyan]")
            for suggestion in safety_result.suggestions:
                print(f"  • {suggestion}")
    
    if safety_result.risk_level != RiskLevel.SAFE:
        confirm_msg = CommandSafety().get_confirmation_message(safety_result)
        print(f"\n[bold]{confirm_msg}[/bold]")
        
        user_confirm = input("> ").strip()
        return CommandSafety().validate_confirmation(user_confirm, safety_result.risk_level)
    
    return True

def handle_cd(command: str, current_dir: str) -> tuple[bool, str]:
    parts = command.strip().split()
    if not parts or parts[0] != "cd":
        return False, current_dir

    target = parts[1] if len(parts) > 1 else os.path.expanduser("~")
    target = os.path.expanduser(target)
    
    if not os.path.isabs(target):
        target = os.path.normpath(os.path.join(current_dir, target))
    if not os.path.isdir(target):
        print(f"[red]cd: no such directory: {target}[/red]")
        return True, current_dir
    return True, target

def main():
    print("[bold green]AI-Enabled Terminal[/bold green]")
    print("[dim]Type your request (type 'exit' to quit)[/dim]\n")

    history = FileHistory(HISTORY_FILE)
    previous_cmds = load_previous_commands()
    session = PromptSession(history=history)

    current_dir = os.getcwd()

    while True:
        completer = FuzzyWordCompleter(previous_cmds)
        try:
            user_input = session.prompt(f"{current_dir} > ", completer=completer).strip()
        except KeyboardInterrupt:
            print("\n[blue]Use 'exit' to quit[/blue]")
            continue
        except EOFError:
            break

        if user_input.lower() in {"exit", "quit"}:
            break

        if not user_input:
            continue

        handled, current_dir = handle_cd(user_input, current_dir)
        if handled:
            continue

        if shell_command(user_input):
            output, success = run_command(user_input, cwd=current_dir)
            
            if success:
                print(output)
                save_command(user_input)
                previous_cmds.append(user_input)
                continue

        try:
            result: CommandResponse = commands(user_input, current_dir)
            
            print(f"\n[cyan]Command:[/cyan] {result.command}")
            print(f"[yellow]Explanation:[/yellow] {result.explanation}")

            final_cmd = result.command
            
            if placeholders(final_cmd):
                print(f"[yellow]Please edit before execution:[/yellow]")
                final_cmd = edit_command(final_cmd)
            else:
                opt = input("Edit command before executing? [y/N]: ").strip().lower()
                if opt == "y":
                    final_cmd = edit_command(final_cmd)

            safety_result = CommandSafety().analyse_command(final_cmd)
            
            if safety_result.risk_level == RiskLevel.SAFE:
                print(f"\n[green]Command approved! Executing...[/green]")
                output, success = run_command(final_cmd, cwd=current_dir)
                print(output)
                
                if success:
                    save_command(final_cmd)
                    previous_cmds.append(final_cmd)
                else:
                    print(f"[red]Command failed to execute[/red]")
            else:   
                confirm_msg = CommandSafety().get_confirmation_message(safety_result)
                print(f"\n[bold]{confirm_msg}[/bold]")
                
                user_confirm = input("> ").strip()
                if CommandSafety().validate_confirmation(user_confirm, safety_result.risk_level):
                    print(f"\n[green]Command approved! Executing...[/green]")
                    output, success = run_command(final_cmd, cwd=current_dir)
                    print(output)
                    
                    if success:
                        save_command(final_cmd)
                        previous_cmds.append(final_cmd)
                    else:
                        print(f"[red]Command failed to execute[/red]")
                else:
                    print(f"[blue]Command rejected by user[/blue]")

        except Exception as e:
            print(f"[red]Error generating suggestion:[/red] {e}")
            print(f"[yellow]Try rephrasing your request[/yellow]")

if __name__ == "__main__":
    main()