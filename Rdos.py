# restart_and_run_rdos.py
# Windows only

import os
import shutil
import subprocess
from pathlib import Path

# Startup folder
startup_folder = Path(
    os.getenv("APPDATA")
) / r"Microsoft\Windows\Start Menu\Programs\Startup"

startup_script = startup_folder / "find_and_run_rdos.py"

python_exe = shutil.which("python") or "python"

# This script runs AFTER reboot
startup_code = f'''
import os
import subprocess

TARGET = "Rdos.py"

def find_file(filename):
    drives = [f"{{d}}:\\\\" for d in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" if os.path.exists(f"{{d}}:\\\\")]

    for drive in drives:
        for root, dirs, files in os.walk(drive):
            if filename in files:
                return os.path.join(root, filename)

    return None

path = find_file(TARGET)

if path:
    folder = os.path.dirname(path)

    subprocess.Popen(
        [r"{python_exe}", path],
        cwd=folder
    )
'''

# Save startup script
with open(startup_script, "w", encoding="utf-8") as f:
    f.write(startup_code)

print("Startup script installed.")
print("Restarting PC in 5 seconds...")

# Restart the PC
subprocess.run("shutdown /r /t 5", shell=True)