import subprocess
import os
import sys
import shutil
import platform
import struct
import textwrap
from pathlib import Path
from app.constants.config import PACKAGE_NAME, APP_VERSION, APP_NAME

class BuildSystem:
    """Sistema de build optimizado para generar binarios multiplataforma 64-bit"""
    
    ARCH_MAP = {
        'x86_64': 'x86_64', 'amd64': 'x86_64', 'x64': 'x86_64',
        'aarch64': 'arm64', 'arm64': 'arm64', 'armv7l': 'armv7l'
    }
    
    def __init__(self):
        self.venv_path = sys.prefix
        self.arch_suffix = self._get_architecture_suffix()
        
    def _get_architecture_suffix(self):
        """Devuelve el sufijo de arquitectura basado en la arquitectura real"""
        arch = platform.machine().lower()
        suffix = self.ARCH_MAP.get(arch, arch)
        print(f"🏗️  Sufijo de arquitectura detectado: {suffix}")
        return suffix
    
    def _get_binary_base_name(self, extension=""):
        """Genera el nombre base del binario con versión y arquitectura"""
        base_name = f"{PACKAGE_NAME}_{APP_VERSION}_{self.arch_suffix}"
        return f"{base_name}{extension}"
    
    def get_binary_name(self):
        """Nombre del binario Linux"""
        binary_name = self._get_binary_base_name()
        print(f"📝 Nombre de binario generado: {binary_name}")
        return binary_name
    
    def get_appimage_name(self):
        """Nombre del AppImage"""
        appimage_name = self._get_binary_base_name(".AppImage")
        print(f"📝 Nombre de AppImage generado: {appimage_name}")
        return appimage_name
    
    def get_exe_name(self):
        """Nombre del ejecutable Windows"""
        arch = self.arch_suffix
        if arch == 'x86_64': arch = 'x64'
        elif arch == 'arm64': arch = 'arm64'
        
        exe_name = f"{PACKAGE_NAME}_{APP_VERSION}_{arch}.exe"
        print(f"📝 Nombre de EXE generado: {exe_name}")
        return exe_name

    def _run_command(self, cmd, error_msg=""):
        """Ejecuta un comando y maneja errores"""
        print(f"Ejecutando: {' '.join(cmd)}")
        try:
            subprocess.run(cmd, check=True)
            return True
        except subprocess.CalledProcessError:
            if error_msg:
                raise RuntimeError(error_msg)
            return False

    def _verify_venv(self):
        """Verifica que estamos en un entorno virtual"""
        in_venv = (hasattr(sys, 'real_prefix') or 
                   (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix))
        if not in_venv:
            raise RuntimeError("❌ NO estás en un entorno virtual. Activa el venv primero.")
        
        if self.venv_path not in sys.executable:
            raise RuntimeError(f"❌ Python ejecutable no está en el venv: {sys.executable}")
        
        try:
            import PyInstaller
            if self.venv_path not in PyInstaller.__file__:
                raise RuntimeError(f"❌ PyInstaller no está en el venv: {PyInstaller.__file__}")
        except ImportError:
            raise RuntimeError("❌ PyInstaller no está instalado en el entorno virtual")
        
        print("✅ Aislamiento total del entorno virtual confirmado")

    def _verify_64bit(self):
        """Verifica que estamos en un entorno 64-bit"""
        python_bits = struct.calcsize("P") * 8
        if python_bits != 64:
            raise RuntimeError(f"Python no es 64-bit (es {python_bits}-bit)")
        
        valid_64bit_arches = ['x86_64', 'amd64', 'x64', 'aarch64', 'arm64']
        arch = platform.machine().lower()
        
        if arch not in valid_64bit_arches:
            raise RuntimeError(f"Arquitectura no soportada: {arch}. Se requiere 64-bit")
        
        print(f"✅ Arquitectura 64-bit confirmada: {arch}")

    def _get_base_pyinstaller_cmd(self, binary_name, icon_path, is_windows=False):
        """Comando base de PyInstaller"""
        sep = ";" if is_windows else ":"
        cmd = [
            sys.executable, "-m", "PyInstaller",
            "main.py", "--onefile", "--windowed", "--clean",
            f"--name={binary_name}", f"--icon={icon_path}",
            f"--add-data=assets{sep}assets", f"--add-data=app{sep}app"
        ]
        return cmd

    def _verify_environment(self):
        """Verificaciones del entorno"""
        self._verify_venv()
        self._verify_64bit()
        
        # Verificar PyInstaller
        self._run_command(
            [sys.executable, "-m", "PyInstaller", "--version"],
            "PyInstaller no está instalado en el entorno virtual."
        )

    def build_linux_binary(self):
        """Genera un binario Linux 64-bit usando PyInstaller DEL ENTORNO VIRTUAL"""
        print("🐧 Generando binario Linux 64-bit...")
        self._verify_environment()
        
        binary_name = self.get_binary_name()
        cmd = self._get_base_pyinstaller_cmd(binary_name, "assets/logo/png/logo_512.png")
        
        # PyInstaller maneja automáticamente las dependencias del venv
        # No necesitamos buscar librerías manualmente
        
        self._run_command(cmd)
        print(f"✅ Binario Linux 64-bit generado en dist/{binary_name}")

    def build_appimage(self):
        """Empaqueta el binario en un AppImage 64-bit"""
        print("📦 Generando AppImage 64-bit...")
        self._verify_environment()

        binary_name = self.get_binary_name()
        appimage_name = self.get_appimage_name()
        binary_path = f"dist/{binary_name}"
        appdir = "AppDir"

        if not os.path.exists(binary_path):
            raise RuntimeError(f"❌ No se encontró el binario {binary_path}. Ejecuta primero la opción 1.")

        # Crear estructura AppDir
        Path(f"{appdir}/usr/bin").mkdir(parents=True, exist_ok=True)
        shutil.copy(binary_path, f"{appdir}/usr/bin/{binary_name}")

        # Crear AppRun
        apprun_content = textwrap.dedent(f"""\
            #!/bin/sh
            HERE="$(dirname "$(readlink -f "$0")")"
            ARCH="$(uname -m)"
            if [ "$ARCH" != "x86_64" ] && [ "$ARCH" != "aarch64" ]; then
                echo "ERROR: Esta aplicación requiere arquitectura 64-bit (x86_64 o aarch64)"
                echo "Arquitectura detectada: $ARCH"
                exit 1
            fi
            exec "$HERE/usr/bin/{binary_name}" "$@"
        """)
        
        apprun_path = Path(appdir) / "AppRun"
        apprun_path.write_text(apprun_content)
        apprun_path.chmod(0o755)

        # Crear .desktop
        desktop_content = textwrap.dedent(f"""\
            [Desktop Entry]
            Type=Application
            Name={APP_NAME} v{APP_VERSION}
            Exec=usr/bin/{binary_name}
            Icon=logo_512
            Comment=Application v{APP_VERSION} built for 64-bit systems
            Categories=Utility;
        """)
        (Path(appdir) / f"{PACKAGE_NAME}.desktop").write_text(desktop_content)

        # Copiar ícono
        shutil.copy("assets/logo/png/logo_512.png", f"{appdir}/logo_512.png")

        # Generar AppImage
        self._run_command(["appimagetool", appdir, appimage_name])
        print(f"✅ AppImage 64-bit generado correctamente: {appimage_name}")

    def build_exe(self):
        """Genera un .exe para Windows 64-bit usando exclusivamente el entorno virtual"""
        print("🪟 Generando .exe Windows 64-bit...")
        self._verify_environment()
        
        binary_name = self.get_exe_name().replace('.exe', '')
        cmd = self._get_base_pyinstaller_cmd(binary_name, "assets/logo/ico/logo_128.ico", True)
        
        self._run_command(cmd)
        print(f"✅ .exe Windows 64-bit generado en dist/{binary_name}.exe")

    def clean_build(self):
        """Limpia los archivos generados por PyInstaller"""
        folders_to_remove = ['build', 'dist']
        spec_files = [f for f in os.listdir('.') 
                     if f.endswith('.spec') and PACKAGE_NAME in f]
        
        for folder in folders_to_remove:
            if os.path.exists(folder):
                shutil.rmtree(folder)
                print(f"🗑️  Eliminada carpeta: {folder}")
        
        for spec_file in spec_files:
            if os.path.exists(spec_file):
                os.remove(spec_file)
                print(f"🗑️  Eliminado archivo: {spec_file}")

    def show_environment_info(self):
        """Muestra información del entorno"""
        arch = platform.machine()
        bits = struct.calcsize("P") * 8
        in_venv = (hasattr(sys, 'real_prefix') or 
                   (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix))
        
        print(f"🏗️  Arquitectura: {arch} ({bits}-bit)")
        print(f"📦 Versión: {APP_VERSION}")
        print(f"🐍 Entorno virtual: {'✅ ACTIVADO' if in_venv else '❌ DESACTIVADO'}")
        if in_venv:
            print(f"📁 Ruta del venv: {self.venv_path}")

def main():
    builder = BuildSystem()
    builder.show_environment_info()
    
    print("\n🚀 Sistema de Build 64-bit (AISLADO EN VENV)")
    print("Selecciona el tipo de build a generar:")
    print("1) Binario Linux 64-bit (para AppImage)")
    print("2) Crear .AppImage 64-bit (empaquetar todo)")
    print("3) .exe Windows 64-bit")
    print("4) Limpiar builds anteriores")

    choice = input("Ingresa 1, 2, 3 o 4: ").strip()

    try:
        if choice == "1":
            builder.build_linux_binary()
        elif choice == "2":
            builder.build_appimage()
        elif choice == "3":
            builder.build_exe()
        elif choice == "4":
            builder.clean_build()
        else:
            print("❌ Opción inválida. Por favor ingresa 1, 2, 3 o 4.")
    except RuntimeError as e:
        print(f"💥 ERROR CRÍTICO: {e}")
        print("💡 Solución: Activa el entorno virtual y verifica las dependencias")
    except Exception as e:
        print(f"💥 Error inesperado: {e}")

if __name__ == "__main__":
    main()