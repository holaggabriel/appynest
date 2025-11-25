# app/utils/usb_detector.py
import os
import sys
from pathlib import Path

def is_running_from_usb() -> bool:
    """
    Detecta si la aplicación se está ejecutando desde una unidad USB/removable
    """
    try:
        app_path = Path(sys.executable if getattr(sys, 'frozen', False) else sys.argv[0]).resolve()
        print(f"[USB-DETECT] Ruta ejecutable: {app_path}")

        # En Windows
        if os.name == 'nt':
            import ctypes

            drive = app_path.drive + '\\'
            print(f"[USB-DETECT] Drive detectado: {drive}")

            try:
                drive_type = ctypes.windll.kernel32.GetDriveTypeW(drive)
                print(f"[USB-DETECT] Tipo de drive: {drive_type} (2=USB, 5=CD-ROM, 4=RED)")
            except Exception as e:
                print(f"[USB-DETECT] ERROR al obtener tipo de drive: {e}")
                return False

            # DRIVE_REMOVABLE = 2, DRIVE_CDROM = 5, DRIVE_REMOTE = 4
            is_removable = drive_type in [2, 5, 4]
            not_home = not app_path.is_relative_to(Path.home())

            print(f"[USB-DETECT] ¿Es unidad removible? {is_removable}")
            print(f"[USB-DETECT] ¿Está fuera del home? {not_home}")

            result = is_removable and not_home
            print(f"[USB-DETECT] Resultado final: {result}")
            return result

        # En Linux/macOS - verificar si está en /media, /mnt, /Volumes
        else:
            usb_paths = ['/media', '/mnt', '/Volumes']
            print(f"[USB-DETECT] Rutas USB posibles: {usb_paths}")

            app_path_str = str(app_path)
            print(f"[USB-DETECT] Comparando contra rutas...")

            for path in usb_paths:
                if app_path_str.startswith(path):
                    print(f"[USB-DETECT] Coincide con ruta USB: {path}")
                    print("[USB-DETECT] Resultado final: True")
                    return True

            print("[USB-DETECT] No coincide con rutas USB. Resultado final: False")
            return False

    except Exception as e:
        print(f"[USB-DETECT] ERROR GENERAL: {e}")
        return False
