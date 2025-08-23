import re
from typing import List, Optional
from dataclasses import dataclass
from enum import Enum

class RiskLevel(Enum):
    SAFE = 'safe'
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'
    CRITICAL = 'critical'

@dataclass
class SafetyResult:
    risk_level: RiskLevel
    warning: List[str]
    blocked: bool = False
    suggestions: Optional[List[str]] = None

class CommandSafety:
    """Analyzes commands for potential risks and provides warnings."""
    
    CRITICAL_PATTERNS = [
        r'\brm\s+-rf\s+/',                       # rm -rf /
        r'\bdd\s+.*of=/dev/',                    # dd to device
        r'\bmkfs\.',                             # filesystem creation
        r'\bfdisk\b.*-d',                        # disk partitioning with delete
        r':\(\)\{\s*:\|:\&\s*\}',                # fork bomb
        r'\bchmod\s+777\s+/',                    # chmod 777 on root
    ]
    
    HIGH_RISK_PATTERNS = [
        r'\brm\s+-rf\s+\*',                      # rm -rf *
        r'\brm\s+-rf\s+\.',                      # rm -rf .
        r'\bsudo\s+rm\s+-rf',                    # sudo rm -rf anything
        r'\bchmod\s+-R\s+777',                   # recursive 777
        r'\bdd\s+if=/dev/urandom',               # random data writing
        r'\b>\s*/dev/sd[a-z]',                   # direct write to disk
        r'\bkillall\s+-9',                       # force kill all processes
        r'\bpkill\s+-9',                         # force kill by name
    ]
    
    MEDIUM_RISK_PATTERNS = [
        r'\brm\s+-rf\s+[^/\s]',                  # rm -rf something specific
        r'\bsudo\s+.*',                          # any sudo command
        r'\bchown\s+-R',                         # recursive ownership change
        r'\bchmod\s+-R',                         # recursive permission change
        r'\bcrontab\s+-r',                       # remove all cron jobs
        r'\biptables\s+-F',                      # flush firewall rules
        r'\bkill\s+-9',                          # force kill process
        r'\bumount\s+.*force',                   # force unmount
    ]
    
    LOW_RISK_PATTERNS = [
        r'\bapt\s+remove',                       # package removal
        r'\byum\s+remove',                       # package removal
        r'\bpip\s+uninstall',                    # python package removal
        r'\bnpm\s+uninstall',                    # node package removal
        r'\bgit\s+reset\s+--hard',               # git hard reset
        r'\bgit\s+clean\s+-fd',                  # git force clean
        r'\bmv\s+.*\s+/tmp',                     # moving to tmp
    ]
    
    def analyse_command(self, command: str) -> SafetyResult:
        command = command.strip().lower()
        warning = []
        suggestions = []

        for pattern in self.CRITICAL_PATTERNS:
            if re.search(pattern, command, re.IGNORECASE):
                warning.append(f"CRITICAL: This command can cause irreversible system damage!")
                return SafetyResult(
                    risk_level=RiskLevel.CRITICAL,
                    warning=warning,
                    blocked=True,
                    suggestions=suggestions
                )

        for pattern in self.HIGH_RISK_PATTERNS:
            if re.search(pattern, command, re.IGNORECASE):
                warning.append(f"HIGH RISK: This command can cause significant damage or data loss")
                if "rm -rf" in command:
                    suggestions.append("Consider using 'trash' or 'mv to backup' instead")
                if "sudo" in command:
                    suggestions.append("Double-check you need elevated privileges")
                return SafetyResult(
                    risk_level=RiskLevel.HIGH,
                    warning=warning,
                    blocked=True,
                    suggestions=suggestions
                )

        for pattern in self.MEDIUM_RISK_PATTERNS:
            if re.search(pattern, command, re.IGNORECASE):
                warning.append(f"MEDIUM RISK: This command can cause significant changes")
                return SafetyResult(
                    risk_level=RiskLevel.MEDIUM,
                    warning=warning,
                    blocked=False,
                    suggestions=suggestions
                )

        for pattern in self.LOW_RISK_PATTERNS:
            if re.search(pattern, command, re.IGNORECASE):
                warning.append(f"LOW RISK: This command may cause data loss or changes")
                return SafetyResult(
                    risk_level=RiskLevel.LOW,
                    warning=warning,
                    blocked=False,
                    suggestions=suggestions
                )
        
        return SafetyResult(
            risk_level= RiskLevel.SAFE,
            warning=[],
            suggestions=[]
        )

    def get_confirmation_message(self, safety_result: SafetyResult) -> str:
        """Generate appropriate confirmation message based on risk level."""
        if safety_result.risk_level == RiskLevel.CRITICAL:
            return "BLOCKED: Command is too dangerous to execute"
        elif safety_result.risk_level == RiskLevel.HIGH:
            return "HIGH RISK: Type 'YES' (in caps) to confirm"
        elif safety_result.risk_level == RiskLevel.MEDIUM:
            return "MEDIUM RISK: Type 'yes' to confirm"
        elif safety_result.risk_level == RiskLevel.LOW:
            return "Are you sure? [y/N]"
        else:
            return "Run this command? [y/N]"

    def validate_confirmation(self, confirmation: str, risk_level: RiskLevel) -> bool:
        """Validate user confirmation based on risk level."""
        confirmation = confirmation.strip()
        
        if risk_level == RiskLevel.CRITICAL:
            return False  # Never allow critical commands
        elif risk_level == RiskLevel.HIGH:
            return confirmation == "YES"
        elif risk_level == RiskLevel.MEDIUM:
            return confirmation == "yes"
        elif risk_level == RiskLevel.LOW:
            return confirmation.lower() in ["y", "yes"]
        else:
            return confirmation.lower() in ["y", "yes"]
    