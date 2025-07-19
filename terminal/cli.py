import os
from executor import command_response, run_command
from agent import commands
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from prompt_toolkit.completion import FuzzyWordCompleter
from rich import print

HISTORY_FILE = os.path.expanduser("~/.ai_terminal_history")

def load_previous_commands():
    if not os.path.exists(HISTORY_FILE):
        return []
    with open(HISTORY_FILE, "r") as file:
        return list(set([line.strip() for line in file if line.strip()]))

def save_command(cmd: str):
    with open(HISTORY_FILE, "a") as file:
        file.write(cmd + "\n")

def main():
    print("[bold green]Type your request (type 'exit' to quit).[/bold green]")

    history = FileHistory(HISTORY_FILE)
    previous_cmds = load_previous_commands()
    session = PromptSession(history=history)

    while True:
        completer = FuzzyWordCompleter(previous_cmds)
        try:
            user_input = session.prompt("> ", completer=completer).strip()
        except KeyboardInterrupt:
            continue
        except EOFError:
            break

        if user_input.lower() in {"exit", "quit"}:
            break

        try:
            result: command_response = commands(user_input)
            print(f"\n[cyan]Suggested Command:[/cyan] {result.command}")
            print(f"[yellow]Explanation:[/yellow] {result.explanation}")

            confirm = input("Run this command? [y/N]: ").strip().lower()

            if confirm == "y":
                output = run_command(result.command)
                print(output)
                save_command(result.command)
                previous_cmds.append(result.command)
            else:
                print("[blue]Command skipped.[/blue]")

        except Exception as e:
            print(f"[red]Error:[/red] {e}")

if __name__ == "__main__":
    main()