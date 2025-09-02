shell_commands = {
    "file_directory": [
        "ls", "cd", "pwd", "mkdir", "rmdir", "rm", "cp", "mv", "touch", "tree",
        "basename", "dirname", "realpath", "stat", "ln", "link", "readlink",
        "chmod", "chown", "chgrp", "umask", "file", "wc", "sort", "uniq"
    ],

    "file_viewing_editing": [
        "cat", "less", "more", "head", "tail", "nano", "vim", "emacs",
        "open",        # macOS only
        "xdg-open"     # Linux only
    ],

    "searching_filtering": [
        "grep", "egrep", "fgrep", "find", "locate", "which", "whereis", "xargs",
        "ack", "ag", "rg", "fd", "fzf", "ripgrep", "jq", "yq"
    ],

    "permissions": [
        "chmod", "chown", "chgrp", "umask", "chattr", "lsattr", "getfacl", "setfacl"
    ],

    "system_info_monitoring": [
        "uname", "uptime", "whoami", "id", "df", "du", "top", "htop", "ps",
        "kill", "killall", "systemctl", "launchctl", "free", "vm_stat",
        "clear", "dmesg", "lscpu", "lsblk", "mount", "umount", "env", "printenv",
        "hostname", "arch", "lsof", "netstat", "ss", "iostat", "vmstat", "sar",
        "strace", "ltrace", "time", "watch", "tee", "script"
    ],

    "networking": [
        "ping", "curl", "wget", "scp", "sftp", "ssh", "ftp",
        "ifconfig", "ip", "netstat", "ss", "traceroute", "dig", "nslookup",
        "networksetup", "arp", "route", "nmap", "telnet", "nc", "netcat",
        "rsync", "socat", "mtr", "iftop", "nethogs", "bandwhich"
    ],

    "archiving_compression": [
        "tar", "gzip", "gunzip", "bzip2", "bunzip2", "xz", "unxz",
        "zip", "unzip"
    ],

    "package_managers": {
        "linux": [
            "apt", "apt-get", "dpkg",
            "yum", "dnf", "zypper", "pacman", "emerge", "snap", "flatpak"
        ],
        "macos": [
            "brew", "port", "softwareupdate"
        ]
    },

    "dev_tools": [
        "git", "docker", "kubectl",
        "python", "python3", "pip", "pip3",
        "node", "npm", "yarn", "npx",
        "gcc", "make", "cmake", "cargo", "rustc", "go", "java", "javac",
        "mvn", "gradle", "sbt", "composer", "gem", "bundle", "stack",
        "cabal", "opam", "vcpkg", "conan"
    ],

    "user_system_management": [
        "sudo", "adduser", "useradd", "passwd", "who", "w", "last", "groups",
        "logout", "shutdown", "reboot", "su", "users"
    ],

    "shell_builtins": [
        "alias", "unalias", "history", "export", "set", "unset",
        "echo", "printf", "read", "true", "false", "type"
    ],

    "job_control": [
        "jobs", "fg", "bg", "disown", "wait", "kill", "sleep"
    ],

    "clipboard_macos": [
        "pbcopy", "pbpaste", "say"
    ],

    "clipboard_linux": [
        "xclip", "xsel"
    ],
    
    "text_processing": [
        "sed", "awk", "cut", "paste", "join", "split", "tr", "fold",
        "fmt", "nl", "pr", "column", "expand", "unexpand"
    ],
    
    "process_management": [
        "nice", "renice", "nohup", "screen", "tmux", "at", "cron", "crontab",
        "bg", "fg", "jobs", "disown", "wait", "timeout", "setsid"
    ],
    
    "disk_storage": [
        "fdisk", "parted", "gparted", "mkfs", "fsck", "badblocks",
        "smartctl", "hdparm", "dd", "pv", "rsync", "ddrescue"
    ],
    
    "security": [
        "gpg", "ssh-keygen", "openssl", "certbot", "letsencrypt",
        "ufw", "iptables", "firewalld", "selinux", "apparmor"
    ],
    
    "monitoring_logs": [
        "journalctl", "logrotate", "logwatch", "fail2ban", "auditd",
        "prometheus", "grafana", "zabbix", "nagios"
    ],
    
    "container_orchestration": [
        "docker", "docker-compose", "podman", "buildah", "skopeo",
        "kubectl", "helm", "k9s", "lens", "rancher"
    ],
    
    "cloud_tools": [
        "aws", "gcloud", "az", "terraform", "ansible", "puppet", "chef",
        "vagrant", "packer", "cloud-init"
    ]
}