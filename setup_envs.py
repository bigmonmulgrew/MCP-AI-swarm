import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).parent

def run(cmd, cwd=None):
    print(f"Running: {cmd}")
    subprocess.run(cmd, cwd=cwd, shell=True, check=True)

def discover_python_services():
    """Finds all first-level folders that contain a requirements.txt."""
    services = []
    for child in ROOT.iterdir():
        if child.is_dir():
            req = child / "requirements.txt"
            if req.exists():
                services.append(child)
    return services

python_services = discover_python_services()

print("\n=== Discovered Python services ===")
for svc in python_services:
    print(" -", svc.name)

common_path = ROOT / "common"

for service_path in python_services:
    print(f"\n=== Setting up environment for {service_path.name} ===")

    # 1. Create virtual environment
    venv_path = service_path / "venv"
    if not venv_path.exists():
        run("python -m venv venv", cwd=service_path)
    else:
        print("venv already exists for", service_path.name)

    # Select pip binary path
    pip = venv_path / ("Scripts/pip.exe" if os.name == "nt" else "bin/pip")

    # 2. Install common package
    if common_path.exists():
        run(f"{pip} install -e {common_path}")
    else:
        print("WARNING: common package not found!")

    # 3. Install service-specific requirements
    req_file = service_path / "requirements.txt"
    run(f"{pip} install -r requirements.txt", cwd=service_path)

    # 4. Output freeze file
    freeze_file = service_path / "requirements_freeze.txt"
    print("Generating freeze file:", freeze_file)
    out = subprocess.check_output(f"{pip} freeze", cwd=service_path, shell=True).decode()
    freeze_file.write_text(out)

print("\n=== All Python environments are ready! ===")
