import argparse
import os
import re

from rich import print
from rich.console import Console
from rich.markdown import Markdown

from terminal import __version__
from terminal.core.executor import CommandResponse, GeneralResponse, run_command
from terminal.core.agent import process_request
from terminal.safety import check_command_safety
from terminal.commands import check_shell_command
from terminal.utils.loading import LoadingAnimation

from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from prompt_toolkit.completion import FuzzyWordCompleter

from terminal.theme import Theme, get_theme  # Import Theme explicitly


def parse_args():
    parser = argparse.ArgumentParser(
        prog="dwarp",
        description="AI-powered terminal assistant",
    )
    parser.add_argument("--version", action="version", version=f"dwarp {__version__}")
    parser.add_argument("--config", metavar="PATH", help="path to config file")
    parser.add_argument("--model", metavar="NAME", help="override model from config")
    parser.add_argument("--verbose", action="store_true", help="enable debug logging")
    parser.add_argument("--theme", metavar="NAME", help="Theme (catppuccin-latte, catppuccin-frappe, catppuccin-macchiato, catppuccin-mocha, dracula)")
    return parser.parse_args()


HISTORY_FILE = os.path.expanduser("~/.dwarp_history")


def load_previous_commands():
    if not os.path.exists(HISTORY_FILE):
        return []
    with open(HISTORY_FILE, "r") as file:
        return list(set([line.strip() for line in file if line.strip()]))


def save_command(cmd: str):
    with open(HISTORY_FILE, "a") as file:
        file.write(cmd + "\n")


PLACEHOLDER_PATTERNS = [
    r"<[^>]+>",
    r"\b(old|new)[-_]?(file|filename|path|dir)\b",
    r"\b(source|destination)[-_ ]?(file|directory|dir|path)\b",
    r"\bYOUR[_-]?(FILE|PATH|DIR|BRANCH|REPO)\b",
]


def placeholders(cmd: str) -> bool:
    for pat in PLACEHOLDER_PATTERNS:
        if re.search(pat, cmd, flags=re.IGNORECASE):
            return True
    return False


def edit_command(suggested: str, theme: Theme) -> str:
    """Edit a command with theme support."""
    print(f"[{theme.info_style}]Current command:[/{theme.info_style}] {suggested}")
    print(f"[{theme.warning_style}]Edit the command (press Enter to keep as is):[/{theme.warning_style}]")
    edited = input("> ").strip()
    return edited if edited else suggested


def handle_cd(command: str, current_dir: str, theme: Theme) -> tuple[bool, str]:
    """Handle cd command with theme support."""
    parts = command.strip().split()
    if not parts or parts[0] != "cd":
        return False, current_dir

    target = parts[1] if len(parts) > 1 else os.path.expanduser("~")
    target = os.path.expanduser(target)

    if not os.path.isabs(target):
        target = os.path.normpath(os.path.join(current_dir, target))

    if not os.path.isdir(target):
        print(f"[{theme.error_style}]cd: no such directory: {target}[/{theme.error_style}]")
        return True, current_dir

    return True, target


def handle_shell_command(result: CommandResponse, current_dir: str, theme: Theme, console: Console, previous_cmds: list) -> str:
    """Handle shell command responses."""
    print(f"\n[{theme.info_style}]Command:[/{theme.info_style}] {result.command}")
    print(f"[{theme.response_style}]Explanation:[/{theme.response_style}] {result.explanation}")

    final_cmd = result.command

    # Special-case clear/cls to avoid printing raw ANSI sequences
    if final_cmd.strip().lower() in {"clear", "cls"}:
        console.clear()
        return current_dir

    if placeholders(final_cmd):
        print(f"[{theme.warning_style}]Please edit before execution:[/{theme.warning_style}]")
        final_cmd = edit_command(final_cmd, theme)
    else:
        opt = input("Edit command before executing? [y/N]: ").strip().lower()  # Fixed f-string
        if opt == "y":
            final_cmd = edit_command(final_cmd, theme)

    if check_command_safety(final_cmd):
        print(f"\n[{theme.success_style}]Command approved! Executing...[/{theme.success_style}]")
        output, success = run_command(final_cmd, cwd=current_dir)
        print(output)
        if success:
            save_command(final_cmd)
            previous_cmds.append(final_cmd)
        else:
            print(f"[{theme.error_style}]Command failed to execute[/{theme.error_style}]")
        return current_dir
    else:
        print(f"[{theme.info_style}]Command rejected by user[/{theme.info_style}]")
        return current_dir


def handle_general_response(result: GeneralResponse, theme: Theme, console: Console = None) -> str | None:
    """Handle general query responses."""
    print(f"\n[{theme.info_style}]Response:[/{theme.info_style}]")
    
    if "```" in result.content or "**" in result.content or "##" in result.content:
        if console is None:
            console = Console()
        console.print(Markdown(result.content))
    else:
        print(result.content)

    if result.action_required and result.suggested_command:
        print(f"\n[{theme.info_style}]Suggested Command:[/{theme.info_style}] {result.suggested_command}")
        opt = input("Execute this command? [y/N]: ").strip().lower()
        if opt == "y":
            return result.suggested_command
    return None


def main():
    args = parse_args()

    # Get theme first
    theme = get_theme(args.theme)
    
    # Create console
    console = Console()

    # Import config after theme is set (to avoid circular imports)
    from terminal.utils import config as config_module
    if args.config:
        config_module.config = config_module.Config(config_file=args.config)
    if args.model:
        config_module.config.model_override = args.model

    print(f"[{theme.success_style}]dwarp[/{theme.success_style}]")
    print("Type your request (type 'exit' to quit)")
    print("Examples: 'install docker', 'what is Python?', 'write a hello world script'\n")

    history = FileHistory(HISTORY_FILE)
    previous_cmds = load_previous_commands()
    session = PromptSession(history=history)

    current_dir = os.getcwd()

    while True:
        completer = FuzzyWordCompleter(previous_cmds)
        try:
            # Use theme for prompt
            user_input = session.prompt(f"[{theme.prompt_style}]{current_dir}[/{theme.prompt_style}] > ", 
                                       completer=completer).strip()
        except KeyboardInterrupt:
            print(f"\n[{theme.info_style}]Use 'exit' to quit[/{theme.info_style}]")
            continue
        except EOFError:
            break

        if user_input.lower() in {"exit", "quit"}:
            break

        if not user_input:
            continue

        handled, current_dir = handle_cd(user_input, current_dir, theme)
        if handled:
            continue

        # Special-case clear/cls entered directly by the user
        if user_input.strip().lower() in {"clear", "cls"}:
            console.clear()
            previous_cmds.append(user_input)
            save_command(user_input)
            continue

        if check_shell_command(user_input):
            output, success = run_command(user_input, cwd=current_dir)
            if success:
                print(output)
                save_command(user_input)
                previous_cmds.append(user_input)
            continue

        try:
            loading_animation = LoadingAnimation("Thinking")
            loading_animation.start()
            try:
                result = process_request(user_input, current_dir)
            finally:
                loading_animation.stop()

            if isinstance(result, CommandResponse):
                current_dir = handle_shell_command(result, current_dir, theme, console, previous_cmds)
            elif isinstance(result, GeneralResponse):
                suggested_cmd = handle_general_response(result, theme, console)
                if suggested_cmd:
                    output, success = run_command(suggested_cmd, cwd=current_dir)
                    print(f"\n[{theme.success_style}]Executing suggested command...[/{theme.success_style}]")
                    print(output)
                    if success:
                        save_command(suggested_cmd)
                        previous_cmds.append(suggested_cmd)

        except Exception as e:
            print(f"[{theme.error_style}]Error generating response:[/{theme.error_style}] {e}")
            print(f"[{theme.warning_style}]Try rephrasing your request[/{theme.warning_style}]")


if __name__ == "__main__":
    main()