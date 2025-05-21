import subprocess

try:
    version = subprocess.check_output(["gswin64c", "--version"], text=True)
    print(f"Ghostscript version: {version.strip()}")
except FileNotFoundError:
    print("Ghostscript не установлен или не добавлен в PATH!")