# terminal/theme.py

from dataclasses import dataclass
from typing import Dict

@dataclass
class Theme:
    name: str
    prompt_style: str
    response_style: str
    error_style: str
    success_style: str
    info_style: str
    warning_style: str

THEMES: Dict[str, Theme] = {
    "catppuccin-latte": Theme(
        name="Catppuccin Latte",
        prompt_style="#8839ef",  # mauve
        response_style="#4c4f69",  # text
        error_style="#d20f39",     # red
        success_style="#40a02b",   # green
        info_style="#209fb5",      # sapphire
        warning_style="#df8e1d",   # peach
    ),
    "catppuccin-frappe": Theme(
        name="Catppuccin Frappe",
        prompt_style="#ca9ee6",  # mauve
        response_style="#c6d0f5",  # text
        error_style="#e78284",     # red
        success_style="#a6d189",   # green
        info_style="#85c1dc",      # sapphire
        warning_style="#e5c890",   # yellow
    ),
    "catppuccin-macchiato": Theme(
        name="Catppuccin Macchiato",
        prompt_style="#c6a0f6",  # mauve
        response_style="#cad3f5",  # text
        error_style="#ed8796",     # red
        success_style="#a6da95",   # green
        info_style="#7dc4e4",      # sapphire
        warning_style="#eed49f",   # yellow
    ),
    "catppuccin-mocha": Theme(
        name="Catppuccin Mocha",
        prompt_style="#cba6f7",  # mauve
        response_style="#cdd6f4",  # text
        error_style="#f38ba8",     # red
        success_style="#a6e3a1",   # green
        info_style="#89dceb",      # sapphire
        warning_style="#f9e2af",   # yellow
    ),
    "dracula": Theme(
        name="Dracula",
        prompt_style="#bd93f9",  # purple
        response_style="#f8f8f2",  # foreground
        error_style="#ff5555",     # red
        success_style="#50fa7b",   # green
        info_style="#8be9fd",      # cyan
        warning_style="#f1fa8c",   # yellow
    ),
    # Add to theme.py THEMES dict
    "test": Theme(
        name="Test Theme",
        prompt_style="bold bright red",
        response_style="bold bright green", 
        error_style="bold bright yellow",
        success_style="bold bright blue",
        info_style="bold bright cyan",
        warning_style="bold bright magenta",
    ),
}

def get_theme(name: str = None) -> Theme:
    if name is None:
        name = "catppuccin-mocha"  # default
    return THEMES.get(name, THEMES["catppuccin-mocha"])