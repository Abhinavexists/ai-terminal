import os
from executor import CommandResponse, run_command
from agent import commands
from safety import CommandSafety, RiskLevel
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

def main():
    print("[bold green]AI-Enabled Terminal[/bold green]")
    print("[dim]Type your request (type 'exit' to quit)[/dim]\n")

    history = FileHistory(HISTORY_FILE)
    previous_cmds = load_previous_commands()
    session = PromptSession(history=history)

    while True:
        completer = FuzzyWordCompleter(previous_cmds)
        try:
            user_input = session.prompt("> ", completer=completer).strip()
        except KeyboardInterrupt:
            print("\n[blue]Use 'exit' to quit[/blue]")
            continue
        except EOFError:
            break

        if user_input.lower() in {"exit", "quit"}:
            break

        if not user_input:
            continue

        output, success = run_command(user_input)
        
        if success:
            print(output)
            save_command(user_input)
            previous_cmds.append(user_input)
            continue

        try:
            result: CommandResponse = commands(user_input)
            
            print(f"\n[cyan]Command:[/cyan] {result.command}")
            print(f"[yellow]Explanation:[/yellow] {result.explanation}")

            if check_command_safety(result.command):
                print(f"\n[green]Command approved! Executing...[/green]")
                output, success = run_command(result.command)
                print(output)
                
                if success:
                    save_command(result.command)
                    previous_cmds.append(result.command)
                else:
                    print(f"[red]Command failed to execute[/red]")
            else:
                print(f"[blue]Command blocked or rejected by user[/blue]")

        except Exception as e:
            print(f"[red]Error generating suggestion:[/red] {e}")
            print(f"[yellow]Try rephrasing your request[/yellow]")

if __name__ == "__main__":
    main()