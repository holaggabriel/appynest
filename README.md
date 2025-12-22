# Appy Nest
[![Descargar](https://img.shields.io/badge/Descargar-%23E53935?style=for-the-badge)](https://github.com/holaggabriel/appynest/releases)
[![Tutorial](https://img.shields.io/badge/Tutorial-%234CAF50?style=for-the-badge)](https://www.youtube.com/watch?v=GZpypRQ4CbU)
[![Comentarios](https://img.shields.io/badge/Comentarios-%231177BB?style=for-the-badge)](https://forms.gle/LFJCeutHFTiYwAHt8)
[![Apoyar Proyecto](https://img.shields.io/badge/Apoyar%20Proyecto-%23E6C23A?style=for-the-badge)](https://buymeacoffee.com/appynest)

Appy Nest es una aplicación de escritorio que facilita la gestión de dispositivos y aplicaciones Android. Permite realizar tareas comunes como instalar, desinstalar o extraer aplicaciones de forma sencilla mediante ADB.

## 📥 Descarga y uso

* **Descargar la aplicación:**
  [https://github.com/holaggabriel/appynest/releases](https://github.com/holaggabriel/appynest/releases)

* **Ver tutorial en video:**
  [https://www.youtube.com/watch?v=GZpypRQ4CbU](https://www.youtube.com/watch?v=GZpypRQ4CbU)

El tutorial muestra paso a paso cómo configurar ADB y empezar a usar Appy Nest correctamente.

## 👥 Comunidad y soporte

Si deseas contribuir a la mejora del proyecto o compartir tu experiencia:

* **Enviar comentarios o sugerencias:**
  [https://forms.gle/LFJCeutHFTiYwAHt8](https://forms.gle/LFJCeutHFTiYwAHt8)

* **Apoyar el proyecto:**
  [https://buymeacoffee.com/appynest](https://buymeacoffee.com/appynest)

Tu apoyo ayuda a mantener y evolucionar la aplicación.

---

## 💻 Compatibilidad entre sistemas (Linux y Windows)

Appy Nest fue desarrollado originalmente en **Linux**, por lo que algunas funciones pueden tener un rendimiento o compatibilidad ligeramente mejor en este sistema.
En **Windows**, la aplicación funciona correctamente en la mayoría de los casos, pero podrían presentarse pequeños detalles debido a diferencias entre plataformas.

## 🐧 Uso en Linux (AppImage + recomendación)

Si descargas la versión **AppImage**, puedes ejecutarla directamente asignándole permisos:

```bash
chmod +x AppyNest.AppImage
./AppyNest.AppImage
```

Para una **mejor integración con tu sistema** (menús, iconos), se recomienda usar **AppImageLauncher**.

* Puedes **descargarlo desde su página de GitHub**:
  👉 [https://github.com/TheAssassin/AppImageLauncher](https://github.com/TheAssassin/AppImageLauncher) 
* O buscarlo en la **tienda de aplicaciones de tu distribución** (el nombre puede variar según la distro, por ejemplo: “Software”, “Pamac”, “Discover”, “GNOME Software”, etc.).

AppImageLauncher se encargará de gestionar automáticamente tus AppImage sin necesidad de configuraciones manuales.

---

## 🛠️ Para desarrolladores

**Requisitos de Python:** Appy Nest requiere **Python 3.13.x**. Asegúrate de tener instalada esta versión antes de continuar.

Para ejecutar **Appy Nest desde el código fuente**, sigue estos pasos:

1. **Crear el entorno virtual**

   ```bash
   python -m venv venv
   ```

2. **Activar el entorno virtual**

   * En **Linux**:

     ```bash
     source venv/bin/activate
     ```
   * En **Windows (PowerShell)**:

     ```powershell
     venv\Scripts\activate
     ```
   * En **Windows (CMD)**:

     ```cmd
     venv\Scripts\activate.bat
     ```

3. **Instalar las dependencias**

   ```bash
   pip install -r requirements.txt
   ```

4. **Ejecutar la aplicación**

   ```bash
   python main.py
   ```

5. **Ejecutar en modo debug (opcional)**

   Para activar los mensajes de debug, define la variable de entorno `ENV` antes de ejecutar:

   * En **Linux**:

     ```bash
     ENV=dev python main.py
     ```

   * En **Windows (PowerShell)**:

     ```powershell
     $env:ENV="dev"
     python main.py
     ```

   * En **Windows (CMD)**:

     ```cmd
     set ENV=dev
     python main.py
     ```

> Cuando la variable no está definida, la aplicación se ejecuta en modo normal (sin debug).
