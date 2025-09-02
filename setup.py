from setuptools import setup, find_packages

setup(
    name="ai-terminal-cli",
    version="0.1.6",
    description="Terminal assistant built as an open source minimal alternative to Warp",
    author="Abhinav",
    author_email="abhinavkumarsingh2023@gmail.com",
    packages=find_packages(include=["terminal*"]),
    python_requires=">=3.12",
    install_requires=[
        "prompt-toolkit==3.0.51",
        "rich==14.1.0", 
        "pydantic==2.11.7",
        "python-dotenv==1.1.1",
        "google-genai==1.31.0"
    ],
    entry_points={
        "console_scripts": [
            "ai-terminal=terminal.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.12",
        "Topic :: System :: Shells",
        "Topic :: Utilities",
    ],
    keywords=["terminal", "ai", "shell", "assistant", "cli", "gemini"],
)
