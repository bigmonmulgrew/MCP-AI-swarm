import os
import subprocess
from pathlib import Path
from datetime import datetime
import time

PRINT_DELAY = 0.1  # seconds — adjust globally

ROOT = Path(__file__).parent

# ---------------------------------------------------------
# Utility functions
# ---------------------------------------------------------

def slow_print(*args, delay=PRINT_DELAY, **kwargs):
    """Wrapper for slow_print that adds a slight delay for readability."""
    print(*args, **kwargs)
    time.sleep(delay)
    
def run(cmd, cwd=None):
    """Run a shell command and display it."""
    slow_print(f"Running: {cmd}")
    subprocess.run(cmd, cwd=cwd, shell=True, check=True)

def discover_python_services():
    """Find one-level folders that contain requirements.txt."""
    services = []
    for child in ROOT.iterdir():
        if child.is_dir() and (child / "requirements.txt").exists():
            services.append(child)
    return services

def pip_path(venv_path):
    """Return pip path depending on OS."""
    return str(
        venv_path / ("Scripts/pip.exe" if os.name == "nt" else "bin/pip")
    )

def activate_command(venv_path):
    """Return environment activation command."""
    if os.name == "nt":
        return f"{venv_path}\\Scripts\\activate"
    else:
        return f"source {venv_path}/bin/activate"

# ---------------------------------------------------------
# Environment Setup Logic
# ---------------------------------------------------------
def setup_env(service_path):
    """Create/update venv for a service and return summary info."""
    name = service_path.name
    venv_path = service_path / "venv"

    summary = {
        "name": name,
        "path": str(service_path),
        "venv_created": False,
        "requirements_installed": False,
        "common_installed": False,
        "freeze_written": False,
    }

    slow_print(f"\n=== Setting up environment for {name} ===")

    # 1. Create virtual environment
    if not venv_path.exists():
        run("python -m venv venv", cwd=service_path)
        summary["venv_created"] = True
    else:
        slow_print("venv already exists")
    
    pip = pip_path(venv_path)

    # 2. Install common package if present
    common_path = ROOT / "common"
    if common_path.exists():
        run(f"{pip} install -e {common_path}")
        summary["common_installed"] = True
    else:
        slow_print("WARNING: common package not found!")

    # 3. Install service requirements
    req_file = service_path / "requirements.txt"
    if req_file.exists():
        run(f"{pip} install -r requirements.txt", cwd=service_path)
        summary["requirements_installed"] = True

    # 4. Output freeze file
    freeze_file = service_path / "requirements_freeze.txt"
    result = subprocess.check_output(f"{pip} freeze", cwd=service_path, shell=True).decode()
    freeze_file.write_text(result)
    summary["freeze_written"] = True

    return summary

# ---------------------------------------------------------
# Interactive Menu
# ---------------------------------------------------------
def print_summary(summaries):
    slow_print("\n======================================")
    slow_print(" ENVIRONMENT SETUP SUMMARY")
    slow_print("======================================\n")

    for s in summaries:
        slow_print(f"[{s['name']}]")
        slow_print(f"Path: {s['path']}")
        slow_print(f" - venv created:            {s['venv_created']}")
        slow_print(f" - requirements installed:   {s['requirements_installed']}")
        slow_print(f" - common installed:         {s['common_installed']}")
        slow_print(f" - freeze file written:      {s['freeze_written']}")
        slow_print()

def show_menu(services):
    slow_print("\n======================================")
    slow_print(" MCO ENVIRONMENT MANAGER")
    slow_print("======================================")
    slow_print("0. Exit")
    slow_print("1. Update ALL environments")

    offset = 2
    slow_print("\nUpdate single environment:")
    for i, svc in enumerate(services):
        slow_print(f"{i + offset}. Update {svc.name}")

    offset2 = offset + len(services)
    slow_print("\nActivate environment:")
    for i, svc in enumerate(services):
        slow_print(f"{i + offset2}. Activate {svc.name}")

    slow_print("\n======================================")

    choice = input("Select an option: ")
    return choice, offset, offset2

# ---------------------------------------------------------
# Main Script Flow
# ---------------------------------------------------------
if __name__ == "__main__":
    services = discover_python_services()
    summaries = []

    slow_print("\nDiscovered Python environments:")
    for svc in services:
        slow_print(" -", svc.name)

    # Initial setup on script run
    for svc in services:
        summaries.append(setup_env(svc))

    # Print summary
    print_summary(summaries)

    # Interactive menu loop
    while True:
        choice, offset, offset2 = show_menu(services)

        # Exit
        if choice == "0":
            slow_print("Exiting...")
            break

        # Update all
        if choice == "1":
            slow_print("\nUpdating ALL environments...")
            for svc in services:
                setup_env(svc)
            continue

        # Update specific env
        try:
            idx = int(choice)
        except ValueError:
            slow_print("Invalid input")
            continue

        # Update single
        if offset <= idx < offset2:
            svc = services[idx - offset]
            slow_print(f"\nUpdating environment: {svc.name}")
            setup_env(svc)
            continue

        # Activate single
        if offset2 <= idx < offset2 + len(services):
            svc = services[idx - offset2]
            venv_path = svc / "venv"
            cmd = activate_command(venv_path)

            slow_print(f"\nTo activate {svc.name} via terminal, run:")
            slow_print(f"  {cmd}\n")

            slow_print("To activate this environment in VS Code:")
            slow_print("  1. Open VS Code in this folder:")
            slow_print(f"       {svc}")
            slow_print("  2. Press Ctrl+Shift+P (Cmd+Shift+P on Mac)")
            slow_print("  3. Type: 'Python: Select Interpreter'")
            slow_print("  4. Choose the interpreter located at:")
            if os.name == "nt":
                slow_print(f"       {venv_path}\\Scripts\\python.exe")
            else:
                slow_print(f"       {venv_path}/bin/python")
            slow_print("\nOnce selected, VS Code will automatically use this venv for:")
            slow_print("  - Running Python files")
            slow_print("  - Debugger sessions")
            slow_print("  - IntelliSense and autocomplete")
            slow_print("  - Integrated terminal sessions")
            continue


        slow_print("Invalid option.")
