from executor import run_command, command_response
from agent import commands
from rich import print

def main():
    print("[bold green]Type your request (type 'exit' to quit).[/bold green]")
    while True:
        user_input = input(">").strip()
        if user_input.lower() in {"exit", "quit"}:
            break

        try:
            result: command_response = commands(user_input)
            print(f"\n[cyan]Suggested Command:[/cyan] {result.command}")
            print(f"[yellow]Explanation:[/yellow] {result.explanation}")

            confirm = input("Run this command? [y/N]: ").strip().lower()
            if confirm == "y":
                run_command(result.command)
        except Exception as e:
            print(f"[red]Error:[/red] {e}")

if __name__ == "__main__":
    main()