# build.py
import subprocess
from app.constants.config import PACKAGE_NAME

# Comando PyInstaller
cmd = [
    "pyinstaller",
    "main.py",
    "--onefile",
    "--windowed",
    f"--name={PACKAGE_NAME}",
    "--icon=assets/logo/ico/logo_128.ico",
    "--add-data=assets;assets",
    "--add-data=app;app"
]

subprocess.run(cmd, check=True)
