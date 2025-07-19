import subprocess
from rich import print
from pydantic import BaseModel

class command_response(BaseModel):
    command: str
    explanation: str

def run_command(command: str):
    try:
        result = subprocess.run(command, shell=True, check=True, text=True)
        print(f"[green]Command executed successfully.[/green]")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"[red]Error while executing:[/red] {e.cmd}")
        return e.stderr or ""