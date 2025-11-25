# app/launcher/usb_launcher.py
import os
import sys
import subprocess
import tempfile
import shutil
from pathlib import Path

def launch_detached():
    """
    Copia el .exe al TEMP y lo ejecuta desde allí totalmente desacoplado del USB.
    """
    try:
        # Ruta del ejecutable real del usuario
        real_exe = Path(sys.executable if getattr(sys, "frozen", False) else sys.argv[0]).resolve()
        print(f"[LAUNCHER] Ejecutable real: {real_exe}")

        temp_dir = Path(tempfile.gettempdir()) / "appynest_run"
        temp_dir.mkdir(exist_ok=True)

        temp_exe = temp_dir / real_exe.name
        print(f"[LAUNCHER] Copiando exe a: {temp_exe}")

        # copiar exe
        shutil.copy2(real_exe, temp_exe)

        # ejecutar desde temp
        DETACHED_PROCESS = 0x00000008
        CREATE_NEW_PROCESS_GROUP = 0x00000200
        CREATE_NO_WINDOW = 0x08000000

        print("[LAUNCHER] Ejecutando app desde TEMP...")

        subprocess.Popen(
            [str(temp_exe)] + sys.argv[1:],
            creationflags=DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP | CREATE_NO_WINDOW,
            close_fds=True,
            cwd=str(temp_dir)
        )

        print("[LAUNCHER] Lanzado correctamente. Cerrando proceso original.")
        return True

    except Exception as e:
        print("[LAUNCHER ERROR]", e)
        return False
