import subprocess
import os
import re
from .adb_manager import ADBManager

class APKInstaller:
    def __init__(self, adb_manager: ADBManager):
        self.adb_manager = adb_manager
    
    def _parse_adb_error(self, error_message):
        """Convierte mensajes de error técnicos de ADB en mensajes entendibles para el usuario"""
        error_lower = error_message.lower()
        
        # Patrones de error comunes
        error_patterns = {
            r'missing_split': "Esta aplicación requiere archivos adicionales que no están presentes. Es probable que sea un Split APK.",
            r'install_failed_missing_split': "Faltan componentes de la aplicación. Necesitas instalar todos los archivos de la aplicación.",
            r'no_matching_abis': "La aplicación no es compatible con la arquitectura de tu dispositivo.",
            r'install_failed_no_matching_abis': "Incompatibilidad de arquitectura: la aplicación contiene código nativo que no funciona en tu dispositivo.",
            r'inconsistent_certificates': "Error de certificados: la aplicación ya existe con una firma diferente.",
            r'install_failed_update_incompatible': "No se puede actualizar: versión incompatible o firma diferente.",
            r'install_failed_insufficient_storage': "Espacio insuficiente en el dispositivo.",
            r'insufficient_storage': "No hay suficiente espacio libre en el dispositivo.",
            r'device_not_found': "Dispositivo no encontrado o desconectado.",
            r'device offline': "El dispositivo está desconectado o en modo offline.",
            r'more than one device': "Hay múltiples dispositivos conectados. Especifica cuál usar.",
            r'permission denied': "Permisos insuficientes. Verifica que la depuración USB esté activada.",
            r'timeout': "Tiempo de espera agotado. El dispositivo no respondió.",
            r'application not installed': "La aplicación no se pudo instalar por razones desconocidas.",
        }
        
        # Buscar patrones específicos
        for pattern, user_message in error_patterns.items():
            if re.search(pattern, error_lower):
                return user_message
        
        # Si no encontramos un patrón específico, dar una explicación general
        if "split" in error_lower:
            return "Error de aplicación dividida: Esta aplicación necesita múltiples archivos para instalarse correctamente."
        elif "abi" in error_lower:
            return "Error de compatibilidad: La aplicación no funciona en la arquitectura de tu dispositivo."
        
        return "Error durante la instalación. Verifica que el APK sea compatible con tu dispositivo."

    def _get_simple_error_message(self, stderr, stdout):
        """Extrae el mensaje de error más relevante de la salida de ADB"""
        # Priorizar stderr sobre stdout
        error_output = stderr if stderr else stdout
        
        if not error_output:
            return "Error desconocido durante la instalación"
        
        # Buscar líneas que contengan "error", "failure", o "failed"
        error_lines = []
        for line in error_output.split('\n'):
            line_lower = line.lower()
            if any(keyword in line_lower for keyword in ['error', 'failure', 'failed', 'cannot', 'unable']):
                error_lines.append(line.strip())
        
        # Si encontramos líneas de error específicas, usar la primera
        if error_lines:
            return self._parse_adb_error(error_lines[0])
        
        # Si no, parsear toda la salida
        return self._parse_adb_error(error_output)

    def install_apk(self, apk_path, device_id):
        """Instala un APK en el dispositivo especificado con mensajes de error amigables"""
        try:
            if not os.path.exists(apk_path):
                return False, "El archivo APK no existe o no se puede acceder a él."
            
            apk_name = os.path.basename(apk_path)
            adb_path = self.adb_manager.get_adb_path()
            
            # Verificar que el dispositivo sigue conectado
            check_result = subprocess.run(
                [adb_path, "-s", device_id, "get-state"],
                capture_output=True, text=True, timeout=10
            )
            
            if check_result.returncode != 0:
                return False, "📱 Dispositivo no disponible. Verifica que esté conectado y con depuración USB activada."

            # Instalar el APK
            install_result = subprocess.run(
                [adb_path, "-s", device_id, "install", "-r", apk_path],
                capture_output=True, text=True, timeout=60
            )
            
            if install_result.returncode == 0:
                return True, f"{apk_name} instalado correctamente"
            else:
                simple_error = self._get_simple_error_message(
                    install_result.stderr, 
                    install_result.stdout
                )
                return False, f"Error instalando {apk_name}:\n{simple_error}"
                
        except subprocess.TimeoutExpired:
            return False, "Tiempo de espera agotado. La instalación tardó demasiado."
        except FileNotFoundError:
            return False, "ADB no encontrado. Verifica la configuración del programa."
        except PermissionError:
            return False, "Permisos insuficientes para acceder al archivo APK."
        except Exception as e:
            return False, f"Error inesperado: {str(e)}"

    def install_multiple_apks(self, apk_paths, device_id):
        """Instala múltiples APKs y devuelve un resumen consolidado"""
        try:
            successful_installs = []
            failed_installs = []
            total_apks = len(apk_paths)
            
            for i, apk_path in enumerate(apk_paths, 1):
                apk_name = os.path.basename(apk_path)
                success, message = self.install_apk(apk_path, device_id)
                
                if success:
                    successful_installs.append(apk_name)
                else:
                    failed_installs.append(f"{apk_name}: {message}")
            
            # Construir mensaje de resumen
            success_count = len(successful_installs)
            failed_count = len(failed_installs)
            
            if success_count == total_apks:
                return True, f"Todas las {total_apks} aplicaciones se instalaron correctamente"
            
            elif success_count > 0 and failed_count > 0:
                summary = f"Resultado de la instalación:\n"
                summary += f"{success_count} de {total_apks} aplicaciones instaladas correctamente\n\n"
                summary += "Errores encontrados:\n"
                for error in failed_installs:
                    summary += f"• {error}\n"
                return False, summary
                
            else:  # Todas fallaron
                summary = f"No se pudo instalar ninguna aplicación:\n"
                for error in failed_installs:
                    summary += f"• {error}\n"
                return False, summary
                
        except Exception as e:
            return False, f"Error durante la instalación múltiple: {str(e)}"