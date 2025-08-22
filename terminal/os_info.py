import platform
import os

class OperatingSystem:
    def __init__(self):
        self.os_info = None
        self.packages = None

    def get_os(self):
        if self.os_info is None:
            system = platform.system().lower()

            if system == "linux":
                self.os_info = self.linux()
            elif system == "darwin":
                self.os_info = self.macos()
            elif system == "windows":
                self.os_info = self.windows()
            else:
                raise ValueError(f"Unsupported OS: {system}")
        return self.os_info
    
    def linux(self):
        if os.path.exists("/etc/os-release"):
            with open("/etc/os-release", "r") as file:
                lines = file.readlines()
                os_info = {}

                for line in lines:
                    if "=" in line:
                        key, value = line.strip().split("=", 1)
                        os_info[key] = value.strip('"')

            id = os_info.get("ID", "").lower()
            name = os_info.get("NAME", "").lower()

            if id in ["ubuntu", "debian", "linuxmint", "pop", "elementary"]:
                return {
                    "os": "debian",
                    "distro": id,
                    "package_manager": "apt",
                    "install": "sudo apt install",
                    "update": "sudo apt update",
                    "upgrade": "upgrade",
                    "remove": "sudo apt remove",
                }

            elif id in ["fedora", "rhel", "centos", "rocky", "alma"]:
                return {
                    "os": "fedora",
                    "distro": id,
                    "package_manager": "dnf",
                    "install": "sudo dnf install",
                    "update": "sudo dnf update",
                    "upgrade": "upgrade",
                    "remove": "sudo dnf remove",
                }
            
            elif id in ["arch", "manjaro", "endeavouros"]:
                    return {
                    "os": "arch",
                    "distro": id,
                    "package_manager": "pacman",
                    "install": "sudo pacman -S",
                    "update": "sudo pacman -Sy",
                    "upgrade": "sudo pacman -Syu",
                    "remove": "sudo pacman -R"
                }

            elif id in ["opensuse", "sles"]:
                return {
                    "os": "opensuse",
                    "distro": id,
                    "package_manager": "zypper",
                    "install": "sudo zypper install",
                    "update": "sudo zypper refresh",
                    "upgrade": "sudo zypper update",
                    "remove": "sudo zypper remove"
                }
            
            elif id in ["gentoo"]:
                return {
                    "os": "gentoo",
                    "distro": id,
                    "package_manager": "emerge",
                    "install": "sudo emerge",
                    "update": "sudo emerge -u",
                    "upgrade": "sudo emerge -u",
                    "remove": "sudo emerge -C"
                }
            
            elif id in ["nixos"]:
                return {
                    "os": "nix",
                    "distro": id,
                    "package_manager": "nix",
                    "install": "nix-env -iA",
                    "update": "nix-env -u",
                    "upgrade": "nix-env -u",
                    "remove": "nix-env -e"
                }
            
            elif id in ["freebsd", "openbsd", "netbsd"]:
                return {
                    "os": "bsd",
                    "distro": id,
                    "package_manager": "pkg",
                    "install": "sudo pkg install",
                    "update": "sudo pkg update",
                    "upgrade": "sudo pkg upgrade",
                    "remove": "sudo pkg delete"
                }

            raise ValueError(f"Unsupported Linux distribution: {id} ({name})")
        
        return {
            "os": "linux",
            "distro": "unknown",
            "package_manager": "unknown",
            "install": "unknown",
            "update": "unknown",
            "upgrade": "unknown",
            "remove": "unknown"
        }

    def macos(self):
            return {
                "os": "macos",
                "distro": "macos",
                "package_manager": "brew",
                "install": "brew install",
                "update": "brew update",
                "upgrade": "brew upgrade",
                "remove": "brew uninstall"
            }

    def windows(self):
            return {
                "os": "windows",
                "distro": "windows",
                "package_manager": "choco",
                "install": "choco install",
                "update": "choco update",
                "upgrade": "choco upgrade",
                "remove": "choco uninstall"
            }

    def get_package_manager(self):
        return self.get_os()
    
    def install_command(self, package: str):
        os = self.get_os()

        if os['install'] == "unknown":
            return f"{os['install']} {package}"
        return f"# Unknown package manager for {os['distro']} - please install {package} manually"

    def get_context(self):
        os = self.get_os()
        return f"Operating System: {os['os']}, Distribution: {os['distro']}, Package Manager: {os['package_manager']}"

operating_system = OperatingSystem()