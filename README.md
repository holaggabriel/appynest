# Appy Nest
[![Tutorial](https://img.shields.io/badge/Tutorial-%234CAF50?style=for-the-badge)](TU_URL_DEL_TUTORIAL)
[![Comentarios](https://img.shields.io/badge/Comentarios-%231177BB?style=for-the-badge)](https://forms.gle/LFJCeutHFTiYwAHt8)
[![Apoyar Proyecto](https://img.shields.io/badge/Apoyar%20Proyecto-%23E6C23A?style=for-the-badge)](https://buymeacoffee.com/appynest)

Appy Nest es una aplicación de escritorio que facilita la gestión de dispositivos y aplicaciones Android. Permite realizar tareas comunes como instalar, desinstalar o extraer aplicaciones de forma sencilla mediante ADB.

## Cómo ejecutar el proyecto

Sigue estos pasos para ejecutar **Appy Nest** en tu máquina local:

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
