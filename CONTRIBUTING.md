# Contributing to AI-Terminal

Thanks for your interest in contributing! This guide will help you get started.

## Getting Started

### Prerequisites

- Python 3.12+
- Git
- Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey)

### Setup Development Environment

1. Fork the repository
2. Clone your fork:

   ```bash
   git clone https://github.com/Abhinavexists/ai-terminal.git
   cd ai-terminal
   ```

3. Create virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

4. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Set up API key:

   ```bash
   export GEMINI_API_KEY="your-api-key-here"
   ```

6. Test the setup:

   ```bash
   python -m terminal.cli
   ```

## Making Changes

### Project Structure

```
ai-terminal/
├── terminal/
│   ├── cli.py          # Main interactive interface
│   ├── agent.py        # AI communication
│   ├── executor.py     # Command execution
│   ├── safety.py       # Safety checks
│   ├── gemini.py       # API key management
│   ├── os_info.py      # OS detection
│   └── commands.py     # Shell command definitions
├── scripts/            # Installation scripts
└── pyproject.toml      # Project configuration
```

### Development Workflow

1. Create a feature branch:

   ```bash
   git checkout -b feature-name
   ```

2. Make your changes
3. Test your changes thoroughly
4. Commit with clear messages:

   ```bash
   git commit -m "Add: brief description of changes"
   ```

5. Push and create a pull request

## Code Guidelines

### Python Style

- Follow PEP 8
- Use descriptive variable names
- Add type hints where helpful
- Keep functions focused and small

### Commit Messages

- Use imperative mood: "Add feature" not "Added feature"
- Keep first line under 50 characters
- Add detailed description if needed

### Testing

- Test your changes manually
- Ensure existing functionality still works
- Test on different Linux distributions if possible

## Areas for Contribution

### High Priority

- Windows and macOS support
- Unit tests
- Documentation improvements
- Bug fixes

### Medium Priority

- Command templates and aliases
- Performance optimizations
- Additional safety patterns
- UI/UX improvements

### Low Priority

- Plugin system
- Multi-language support
- Integration with other tools

## Submitting Changes

### Pull Request Process

1. Update documentation if needed
2. Ensure your code follows the style guidelines
3. Write a clear PR description explaining:
   - What changes you made
   - Why you made them
   - How to test them

4. Link any related issues
5. Wait for review and address feedback

### PR Requirements

- Clear description of changes
- No breaking changes without discussion
- Follows coding standards
- Manually tested

## Reporting Issues

### Bug Reports

Include:

- OS and Python version
- Steps to reproduce
- Expected vs actual behavior
- Error messages or logs
- Your configuration (without API keys)

### Feature Requests

Include:

- Clear description of the feature
- Use case and benefits
- Possible implementation approach

## Getting Help

- Check existing [issues](https://github.com/Abhinavexists/ai-terminal/issues)
- Create a new issue for questions
- Tag maintainers if urgent

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and grow
- Follow the project's goals and vision

## Recognition

All contributors will be acknowledged in the project. Significant contributions may earn you commit access.

Thanks for contributing! 🚀
