import subprocess
import os
from app.constants.config import PACKAGE_NAME, APP_VERSION, APP_NAME
import textwrap
import sys
import shutil
import platform
import struct

def get_architecture_suffix():
    """Devuelve el sufijo de arquitectura basado en la arquitectura real"""
    arch = platform.machine().lower()
    
    arch_map = {
        'x86_64': 'x86_64',
        'amd64': 'x86_64', 
        'x64': 'x86_64',
        'aarch64': 'arm64',
        'arm64': 'arm64',
        'armv7l': 'armv7l'
    }
    
    suffix = arch_map.get(arch, arch)
    print(f"🏗️  Sufijo de arquitectura detectado: {suffix}")
    return suffix

def get_binary_name():
    """Genera el nombre del binario con versión y arquitectura"""
    arch_suffix = get_architecture_suffix()
    # Formato: nombre_version_arquitectura
    binary_name = f"{PACKAGE_NAME}_{APP_VERSION}_{arch_suffix}"
    print(f"📝 Nombre de binario generado: {binary_name}")
    return binary_name

def get_appimage_name():
    """Genera el nombre del AppImage con versión y arquitectura"""
    arch_suffix = get_architecture_suffix()
    # Formato: nombre_version_arquitectura.AppImage
    appimage_name = f"{PACKAGE_NAME}_{APP_VERSION}_{arch_suffix}.AppImage"
    print(f"📝 Nombre de AppImage generado: {appimage_name}")
    return appimage_name

def get_exe_name():
    """Genera el nombre del .exe con versión y arquitectura"""
    arch = platform.machine().lower()
    # Para Windows, usar nombres más estándar
    if arch in ['x86_64', 'amd64', 'x64']:
        arch_suffix = 'x64'
    elif arch in ['aarch64', 'arm64']:
        arch_suffix = 'arm64'
    else:
        arch_suffix = arch
    
    # Formato: nombre_version_arquitectura.exe
    exe_name = f"{PACKAGE_NAME}_{APP_VERSION}_{arch_suffix}.exe"
    print(f"📝 Nombre de EXE generado: {exe_name}")
    return exe_name

def strict_venv_verification():
    """Verificación EXTRA estricta del entorno virtual"""
    print("🛡️  Verificando aislamiento total del entorno virtual...")
    
    # 1. Verificar que estamos en un venv
    in_venv = (hasattr(sys, 'real_prefix') or 
               (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix))
    if not in_venv:
        raise RuntimeError("❌ NO estás en un entorno virtual. Activa el venv primero.")
    print("✅ Entorno virtual confirmado")
    
    # 2. Verificar que sys.executable está en el venv
    venv_path = sys.prefix
    if venv_path not in sys.executable:
        raise RuntimeError(f"❌ Python ejecutable no está en el venv: {sys.executable}")
    print("✅ Python ejecutable está en el venv")
    
    # 3. Verificar PyInstaller está en el venv
    try:
        import PyInstaller
        if venv_path not in PyInstaller.__file__:
            raise RuntimeError(f"❌ PyInstaller no está en el venv: {PyInstaller.__file__}")
        print("✅ PyInstaller está en el venv")
    except ImportError:
        raise RuntimeError("❌ PyInstaller no está instalado en el entorno virtual")
    
    # 4. Verificar rutas de sitio
    import site
    for path in site.getsitepackages():
        if venv_path not in path:
            print(f"⚠️  Advertencia: Ruta de sitio fuera del venv: {path}")
    
    print("✅ Aislamiento total del entorno virtual confirmado")

def verify_64bit_environment():
    """Verifica que estamos en un entorno 64-bit"""
    print("🔍 Verificando arquitectura 64-bit...")
    
    # 1. Verificar bits de Python
    python_bits = struct.calcsize("P") * 8
    if python_bits != 64:
        raise RuntimeError(f"Python no es 64-bit (es {python_bits}-bit)")
    print("✅ Python 64-bit confirmado")
    
    # 2. Verificar arquitectura del sistema
    arch = platform.machine().lower()
    valid_64bit_arches = ['x86_64', 'amd64', 'x64', 'aarch64', 'arm64']
    
    if arch not in valid_64bit_arches:
        raise RuntimeError(f"Arquitectura no soportada: {arch}. Se requiere 64-bit")
    print(f"✅ Arquitectura 64-bit confirmada: {arch}")
    
    # 3. Verificar que PyInstaller generará binario 64-bit
    try:
        result = subprocess.run([sys.executable, "-c", "import struct; print(struct.calcsize('P') * 8)"], 
                              capture_output=True, text=True, check=True)
        if result.stdout.strip() != "64":
            raise RuntimeError("PyInstaller generaría binario 32-bit")
        print("✅ PyInstaller configurado para 64-bit")
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Error verificando PyInstaller: {e}")

def find_python_library_venv_only():
    """Busca la librería libpython 64-bit EXCLUSIVAMENTE en el venv."""
    print("🔍 Buscando librería Python SOLO en el entorno virtual...")
    
    # 🔥 VERIFICACIÓN - asegurar que estamos en venv
    if not (hasattr(sys, 'real_prefix') or 
            (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)):
        raise RuntimeError("❌ No se puede buscar librerías fuera del entorno virtual")
    
    # 🔥 SOLO rutas del venv - ELIMINADAS todas las rutas del sistema
    venv_lib_paths = [
        os.path.join(sys.prefix, "lib"),
        os.path.join(sys.prefix, "lib64"),
    ]
    
    libraries_found = []
    
    for lib_path in venv_lib_paths:
        if not os.path.exists(lib_path):
            continue
            
        print(f"🔎 Buscando en venv: {lib_path}")
        for root, dirs, files in os.walk(lib_path):
            for file in files:
                if file.startswith("libpython3") and file.endswith(".so"):
                    full_path = os.path.join(root, file)
                    
                    # 🔥 VERIFICACIÓN CRÍTICA: asegurar que está DENTRO del venv
                    if not full_path.startswith(sys.prefix):
                        print(f"❌ RECHAZADA: Librería fuera del venv: {full_path}")
                        continue
                    
                    libraries_found.append(full_path)
                    print(f"📁 Encontrada en venv: {file}")
                    
                    # Verificar 64-bit
                    if verify_64bit_library(full_path):
                        print(f"✅ Librería 64-bit del venv: {os.path.basename(full_path)}")
                        return full_path
                    else:
                        print(f"❌ Librería no es 64-bit: {file}")
    
    if not libraries_found:
        print("❌ No se encontró libpython en el entorno virtual")
    else:
        print(f"ℹ️  Se encontraron librerías en venv pero ninguna era 64-bit")
    
    return None

def verify_64bit_library(lib_path):
    """Verifica que una librería es 64-bit"""
    try:
        result = subprocess.run(["file", lib_path], 
                              capture_output=True, text=True, check=True)
        return "64-bit" in result.stdout
    except (subprocess.CalledProcessError, FileNotFoundError):
        # Si 'file' no está disponible, verificar por tamaño
        lib_size = os.path.getsize(lib_path)
        # Las librerías 64-bit suelen ser más grandes
        if lib_size > 1000000:  # > 1MB
            print(f"ℹ️  Asumiendo 64-bit por tamaño ({lib_size} bytes)")
            return True
        return False

def build_linux_binary():
    """Genera un binario Linux 64-bit usando PyInstaller DEL ENTORNO VIRTUAL."""
    print("🐧 Generando binario Linux 64-bit...")
    
    # 🔥 VERIFICACIONES ESTRICTAS
    strict_venv_verification()
    verify_64bit_environment()
    
    python_exe = sys.executable
    
    # Verificar PyInstaller en el venv
    try:
        subprocess.run([python_exe, "-m", "PyInstaller", "--version"], 
                      check=True, capture_output=True)
    except subprocess.CalledProcessError:
        raise RuntimeError("PyInstaller no está instalado en el entorno virtual.")
    
    # 🎯 NOMBRE DINÁMICO con versión y arquitectura
    binary_name = get_binary_name()
    
    cmd = [
        python_exe,
        "-m", "PyInstaller",
        "main.py",
        f"--name={binary_name}",
        "--windowed",
        "--icon=assets/logo/png/logo_512.png",
        "--add-data=assets:assets",
        "--add-data=app:app",
        "--onefile",
        "--clean"
    ]
    
    # 🔥 SOLO agregar librería si está en el VENV
    python_lib = find_python_library_venv_only()
    if python_lib:
        cmd.append(f"--add-binary={python_lib}:./")
        print(f"✅ Librería Python del VENV incluida: {os.path.basename(python_lib)}")
    else:
        print("ℹ️  No se incluyó libpython - PyInstaller usará la suya")
    
    print(f"Ejecutando: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)
    print(f"✅ Binario Linux 64-bit generado en dist/{binary_name}")

def build_appimage():
    """Empaqueta el binario en un AppImage 64-bit."""
    print("📦 Generando AppImage 64-bit...")

    # 🔥 VERIFICACIONES ESTRICTAS
    strict_venv_verification()
    verify_64bit_environment()

    # 🎯 NOMBRES DINÁMICOS con versión y arquitectura
    binary_name = get_binary_name()  # ej: "miapp_1.0.0_x86_64"
    appimage_name = get_appimage_name()
    
    appdir = "AppDir"
    binary_path = f"dist/{binary_name}"

    if not os.path.exists(binary_path):
        print(f"❌ No se encontró el binario {binary_path}. Ejecuta primero la opción 1.")
        return

    # 1️⃣ Crear estructura AppDir
    os.makedirs(f"{appdir}/usr/bin", exist_ok=True)

    # 2️⃣ Copiar binario MANTENIENDO el nombre completo
    subprocess.run(["cp", binary_path, f"{appdir}/usr/bin/{binary_name}"], check=True)
    print(f"✅ Binario copiado como: {binary_name}")

    # 3️⃣ Crear AppRun con el nombre completo
    apprun_path = os.path.join(appdir, "AppRun")
    apprun_content = textwrap.dedent(f"""\
        #!/bin/sh
        HERE="$(dirname "$(readlink -f "$0")")"
        # Verificar arquitectura antes de ejecutar
        ARCH="$(uname -m)"
        if [ "$ARCH" != "x86_64" ] && [ "$ARCH" != "aarch64" ]; then
            echo "ERROR: Esta aplicación requiere arquitectura 64-bit (x86_64 o aarch64)"
            echo "Arquitectura detectada: $ARCH"
            exit 1
        fi
        exec "$HERE/usr/bin/{binary_name}" "$@"
    """)
    with open(apprun_path, "w") as f:
        f.write(apprun_content)
    os.chmod(apprun_path, 0o755)

    # 4️⃣ Crear .desktop (puedes mantener PACKAGE_NAME aquí si prefieres)
    desktop_path = os.path.join(appdir, f"{PACKAGE_NAME}.desktop")
    desktop_content = textwrap.dedent(f"""\
        [Desktop Entry]
        Type=Application
        Name={APP_NAME} v{APP_VERSION}
        Exec=usr/bin/{binary_name}
        Icon=logo_512
        Comment=Application v{APP_VERSION} built for 64-bit systems
        Categories=Utility;
    """)
    with open(desktop_path, "w") as f:
        f.write(desktop_content)

    # 5️⃣ Copiar ícono
    os.makedirs(appdir, exist_ok=True)
    subprocess.run(["cp", "assets/logo/png/logo_512.png", f"{appdir}/logo_512.png"], check=True)

    # 6️⃣ Generar AppImage
    subprocess.run(["appimagetool", appdir, appimage_name], check=True)

    print(f"✅ AppImage 64-bit generado correctamente: {appimage_name}")

def build_exe():
    """Genera un .exe para Windows 64-bit usando exclusivamente el entorno virtual."""
    print("🪟 Generando .exe Windows 64-bit...")
    
    # 🔥 VERIFICACIONES ESTRICTAS
    strict_venv_verification()
    verify_64bit_environment()
    
    python_exe = sys.executable
    
    # Verificar que PyInstaller está disponible en el venv
    try:
        subprocess.run([python_exe, "-m", "PyInstaller", "--version"], 
                      check=True, capture_output=True)
    except subprocess.CalledProcessError:
        raise RuntimeError("PyInstaller no está instalado en el entorno virtual.")
    
    # 🎯 NOMBRE DINÁMICO con versión y arquitectura
    binary_name = get_exe_name().replace('.exe', '')  # PyInstaller añade .exe automáticamente
    
    cmd = [
        python_exe,
        "-m", "PyInstaller",
        "main.py",
        "--onefile",
        "--windowed",
        f"--name={binary_name}",
        "--icon=assets/logo/ico/logo_128.ico",
        "--add-data=assets;assets",
        "--add-data=app;app",
        "--clean"
    ]
    
    print(f"Ejecutando: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)
    print(f"✅ .exe Windows 64-bit generado en dist/{binary_name}.exe")

def clean_build():
    """Limpia los archivos generados por PyInstaller."""
    # 🎯 Limpiar todos los nombres posibles (versiones anteriores también)
    folders_to_remove = ['build', 'dist']
    
    # Buscar archivos .spec que coincidan con el patrón del nombre
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

def show_environment_info():
    """Muestra información del entorno"""
    arch = platform.machine()
    bits = struct.calcsize("P") * 8
    in_venv = (hasattr(sys, 'real_prefix') or 
               (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix))
    
    print(f"🏗️  Arquitectura: {arch} ({bits}-bit)")
    print(f"📦 Versión: {APP_VERSION}")
    print(f"🐍 Entorno virtual: {'✅ ACTIVADO' if in_venv else '❌ DESACTIVADO'}")
    if in_venv:
        print(f"📁 Ruta del venv: {sys.prefix}")

def main():
    show_environment_info()
    print("\n🚀 Sistema de Build 64-bit (AISLADO EN VENV)")
    print("Selecciona el tipo de build a generar:")
    print("1) Binario Linux 64-bit (para AppImage)")
    print("2) Crear .AppImage 64-bit (empaquetar todo)")
    print("3) .exe Windows 64-bit")
    print("4) Limpiar builds anteriores")

    choice = input("Ingresa 1, 2, 3 o 4: ").strip()

    try:
        if choice == "1":
            build_linux_binary()
        elif choice == "2":
            build_appimage()
        elif choice == "3":
            build_exe()
        elif choice == "4":
            clean_build()
        else:
            print("❌ Opción inválida. Por favor ingresa 1, 2, 3 o 4.")
    except RuntimeError as e:
        print(f"💥 ERROR CRÍTICO: {e}")
        print("💡 Solución: Activa el entorno virtual y verifica las dependencias")
    except Exception as e:
        print(f"💥 Error inesperado: {e}")

if __name__ == "__main__":
    main()