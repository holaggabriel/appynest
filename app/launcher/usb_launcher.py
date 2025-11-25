# app/launcher/usb_launcher.py
import os
import sys
import subprocess
import tempfile
import shutil
from pathlib import Path

def copy_executable_to_temp():
    real_exe = Path(sys.executable if getattr(sys, "frozen", False) else sys.argv[0]).resolve()
    temp_dir = Path(tempfile.gettempdir()) / "appynest_run"
    temp_dir.mkdir(exist_ok=True)
    temp_exe = temp_dir / real_exe.name
    shutil.copy2(real_exe, temp_exe)
    return temp_exe

def launch_temp_exe(temp_exe):
    DETACHED_PROCESS = 0x00000008
    CREATE_NEW_PROCESS_GROUP = 0x00000200
    CREATE_NO_WINDOW = 0x08000000

    subprocess.Popen(
        [str(temp_exe), "--launched"] + sys.argv[1:],
        creationflags=DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP | CREATE_NO_WINDOW,
        close_fds=True,
        cwd=str(temp_exe.parent)
    )
