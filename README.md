# AI-Terminal

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/platform-linux-lightgrey.svg)](https://github.com/your-username/ai-enabled-terminal)

Terminal assistant which is built as an open source minimal alternative to warp.

## Quick Start

### Prerequisites

- Python 3.12 or higher
- Linux operating system (Ubuntu, Arch, Fedora, CentOS, openSUSE, Debian supported) (Windows and MacOS will be supproted later on)
- Google Gemini API key ([Get one here](https://aistudio.google.com/app/apikey))

### Installation

#### Option 1: Binary Release (Recommended)

1. Download the latest release from [Releases](https://github.com/your-username/ai-enabled-terminal/releases)
2. Extract and install:

   ```bash
   tar -xzf ai-terminal-linux.tar.gz
   cd ai-terminal-linux
   sudo ./install.sh
   ```

3. Launch the terminal:

   ```bash
   ai-terminal
   ```

4. Enter your Gemini API key when prompted

#### Option 2: From Source

1. Clone the repository:

   ```bash
   git clone https://github.com/Abhinavexists/ai-terminal.git
   cd ai-enabled-terminal
   ```

2. Create and activate virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up your API key:

   ```bash
   export GEMINI_API_KEY="your-api-key-here"
   ```

5. Run the application:

   ```bash
   python -m terminal.cli
   ```

## Usage Examples

```bash
# Natural language commands
> install docker
Command: sudo pacman -S docker
Explanation: Installs Docker using the system package manager

> find all python files in current directory
Command: find . -name "*.py" -type f
Explanation: Searches for all Python files in the current directory and subdirectories

> compress folder into zip
Command: zip -r archive.zip folder_name
Explanation: Creates a ZIP archive of the specified folder

> show disk usage sorted by size
Command: du -sh * | sort -hr
Explanation: Shows disk usage of all items in current directory, sorted by size
```

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

## Pending stuff

- [ ] Support for Windows and macOS
- [ ] Custom command templates and aliases
- [ ] Plugin system for extending functionality
- [ ] Command explanation and learning mode
- [ ] Integration with popular development tools
- [ ] Multi-language support

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
