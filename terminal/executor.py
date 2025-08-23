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
            capture_output=True,
            cwd=cwd,
        )
        return result.stdout or "", True
    except subprocess.CalledProcessError as e:
        # Suppress noisy error logs and captured stderr/stdout
        return (e.stdout or e.stderr or ""), False