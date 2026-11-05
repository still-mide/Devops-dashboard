import datetime
import subprocess
import sys

SEPARATOR = "=" * 50
TIMEOUT_SECONDS = 10

# Tracks whether any check failed, so the script can exit non-zero
# (useful when run from cron, CI, or another monitoring tool).
failures = []


def run_command(name, args):
    """Run a command and return its output, or a clear error message.

    Uses an argument list (no shell) and a timeout so a missing or hung
    command can't silently produce empty output or block the monitor.
    """
    try:
        result = subprocess.run(
            args, capture_output=True, text=True, timeout=TIMEOUT_SECONDS
        )
    except FileNotFoundError:
        failures.append(name)
        return f"[unavailable] '{args[0]}' command not found on this system\n"
    except subprocess.TimeoutExpired:
        failures.append(name)
        return f"[unavailable] '{args[0]}' timed out after {TIMEOUT_SECONDS}s\n"

    if result.returncode != 0:
        failures.append(name)
        error = result.stderr.strip() or f"exit code {result.returncode}"
        return f"[error] '{' '.join(args)}' failed: {error}\n"
    return result.stdout


def top_processes(count=5):
    """Return the header line plus the top `count` processes by CPU."""
    output = run_command("processes", ["ps", "aux", "--sort=-%cpu"])
    if output.startswith("["):  # error message from run_command
        return output
    lines = output.splitlines()
    return "\n".join(lines[: count + 1]) + "\n"


def main():
    print(SEPARATOR)
    print("     DEVOPS SYSTEM MONITOR")
    print(SEPARATOR)

    # Get disk
    print("Disk size: ", run_command("disk", ["df", "-h"]))
    print(SEPARATOR)

    # Get memory
    print("Memory size: ", run_command("memory", ["free", "-h"]))
    print(SEPARATOR)

    # Get uptime
    print("uptime: ", run_command("uptime", ["uptime"]))
    print(SEPARATOR)

    # Get processes
    print("processes: ", top_processes())
    print(SEPARATOR)

    # Get date and time
    now = datetime.datetime.now()
    print("Date: ", now.strftime("%Y-%m-%d %H:%M:%S"))

    if failures:
        print(f"WARNING: {len(failures)} check(s) failed: {', '.join(failures)}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
