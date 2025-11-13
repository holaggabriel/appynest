import subprocess

def get_silent_startupinfo():
    """Retorna configuración para ejecutar comandos sin mostrar consola"""
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startupinfo.wShowWindow = 0  # SW_HIDE
    return startupinfo