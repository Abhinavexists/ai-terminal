import subprocess
from pydantic import BaseModel

class CommandResponse(BaseModel):
    command: str
    explanation: str

def run_command(command: str, cwd: str | None = None) -> tuple[str, bool]:
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            text=True,
            cwd=cwd,
        )
        return "Command executed successfully", True
    except subprocess.CalledProcessError as e:
        return f"Command failed with exit code {e.returncode}", False