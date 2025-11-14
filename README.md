# Appy Nest
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

   Para activar los mensajes de debug, define la variable de entorno `APPYNEST_DEBUG` antes de ejecutar:

   * En **Linux**:

     ```bash
     APPYNEST_DEBUG=1 python main.py
     ```

   * En **Windows (PowerShell)**:

     ```powershell
     $env:APPYNEST_DEBUG="1"
     python main.py
     ```

   * En **Windows (CMD)**:

     ```cmd
     set APPYNEST_DEBUG=1
     python main.py
     ```

> Cuando la variable no está definida, la aplicación se ejecuta en modo normal (sin debug).
