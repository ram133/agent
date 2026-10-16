# agent.py
# https://github.com/ram133/agent

import os
import sys
import subprocess
from pathlib import Path

def run_command(command):
    """Execute a shell command and return output."""
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e.stderr.strip()}", file=sys.stderr)
        sys.exit(1)

def main():
    print("Initializing Autonomous Agent Runtime...")
    
    # Ensure working directory context
    repo_root = Path(__file__).parent.resolve()
    os.chdir(repo_root)
    
    # Check git repository status
    branch = run_command("git branch --show-current")
    print(f"Active Git Branch: {branch}")
    
    # Execute autonomous workflow tasks
    print("Running repository validation & context sync...")
    
    # Example agent execution loop placeholder
    print("Agent runtime is ready and operational.")

if __name__ == "__main__":
    main()
