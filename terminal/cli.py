from rich import print
from agent import commands
from executor import run_command

def main():
    print("[bold green]Type your request (type 'exit' to 'quit').[/bold green]")
    while True:
        user_input = input(">").strip()
        if user_input.lower() in {"exit", "quit"}:
            break

        shell_command = commands(user_input)

        if shell_command.lower().startswith("please clarify") or not shell_command.strip():
            print("[red] AI could not understand. Please be more specific.[/red]")

        print(f"[yellow]Suggested command:[/yellow] {shell_command}")
        confirm = input("Run this command? [y/N] ").strip().lower()

        if confirm == "y":
            run_command(shell_command)

if __name__ == "__main__":
    main()
