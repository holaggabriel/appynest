import subprocess
import os
from app.constants.config import PACKAGE_NAME
import textwrap

def build_linux_binary():
    """Genera un binario Linux usando PyInstaller (para AppImage) con la librería de Python del sistema."""
    print("🐧 Generando binario Linux...")

    # Buscar la librería libpython en el sistema
    python_lib = None
    for root, dirs, files in os.walk("/usr/lib"):
        for file in files:
            if file.startswith("libpython3") and file.endswith(".so.1.0"):
                python_lib = os.path.join(root, file)
                break
        if python_lib:
            break

    if not python_lib:
        print("❌ No se encontró la librería de Python en /usr/lib. Instala python-dev o verifica tu instalación de Python.")
        return

    print(f"✅ Librería de Python encontrada en el sistema: {python_lib}")

    # Comando PyInstaller
    cmd = [
        "pyinstaller",
        "main.py",
        f"--name={PACKAGE_NAME}",
        "--windowed",
        "--icon=assets/logo/png/logo_512.png",
        "--add-data=assets:assets",
        "--add-data=app:app",
        "--onefile",
        f"--add-binary={python_lib}:lib/"
    ]

    subprocess.run(cmd, check=True)
    print(f"✅ Binario Linux generado en dist/{PACKAGE_NAME}/ con librería Python embebida correctamente.")

def build_appimage():
    """Empaqueta el binario en un AppImage usando appimagetool."""
    print("📦 Generando AppImage...")

    appdir = "AppDir"
    binary_path = f"dist/{PACKAGE_NAME}"
    appimage_name = f"{PACKAGE_NAME}-x86_64.AppImage"

    if not os.path.exists(binary_path):
        print("❌ No se encontró el binario. Ejecuta primero la opción 2 (Binario Linux).")
        return

    # 1️⃣ Crear estructura AppDir
    os.makedirs(f"{appdir}/usr/bin", exist_ok=True)

    # 2️⃣ Copiar binario
    subprocess.run(["cp", binary_path, f"{appdir}/usr/bin/{PACKAGE_NAME}"], check=True)

    # 3️⃣ Crear AppRun
    apprun_path = os.path.join(appdir, "AppRun")
    apprun_content = textwrap.dedent(f"""\
        #!/bin/sh
        HERE="$(dirname "$(readlink -f "$0")")"
        exec "$HERE/usr/bin/{PACKAGE_NAME}" "$@"
    """)
    with open(apprun_path, "w") as f:
        f.write(apprun_content)
    os.chmod(apprun_path, 0o755)

    # 4️⃣ Crear .desktop
    desktop_path = os.path.join(appdir, f"{PACKAGE_NAME}.desktop")
    desktop_content = textwrap.dedent(f"""\
        [Desktop Entry]
        Type=Application
        Name={PACKAGE_NAME}
        Exec=usr/bin/{PACKAGE_NAME}
        Icon=logo_512
        Categories=Utility;
    """)
    with open(desktop_path, "w") as f:
        f.write(desktop_content)

    # 5️⃣ Copiar ícono
    os.makedirs(appdir, exist_ok=True)
    subprocess.run(["cp", "assets/logo/png/logo_512.png", f"{appdir}/logo_512.png"], check=True)

    # 6️⃣ Generar AppImage
    subprocess.run(["appimagetool", appdir, appimage_name], check=True)

    print(f"✅ AppImage generado correctamente: {appimage_name}")

def build_exe():
    """Genera un .exe para Windows usando PyInstaller."""
    print("Generando .exe...")
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
    print(".exe generado correctamente!")

def main():
    print("Selecciona el tipo de build a generar:")
    print("1) Binario Linux (para AppImage)")
    print("2) Crear .AppImage (empaquetar todo)")
    print("3) .exe (Windows)")

    choice = input("Ingresa 1, 2 o 3: ").strip()

    if choice == "1":
        build_linux_binary()
    elif choice == "2":
        build_appimage()
    elif choice == "3":
        build_exe()
    else:
        print("Opción inválida. Por favor ingresa 1, 2 o 3.")


if __name__ == "__main__":
    main()
