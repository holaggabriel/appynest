from .app_uninstaller import AppUninstaller
from .app_extractor import AppExtractor
from .app_lister import AppLister

class AppManager(AppLister, AppUninstaller, AppExtractor):
    """Clase principal que combina todas las funcionalidades de gestión de aplicaciones"""
    
    def __init__(self, adb_manager):
        # Pasar la misma instancia de ADBManager a todas las subclases
        AppLister.__init__(self, adb_manager)
        AppUninstaller.__init__(self, adb_manager)
        AppExtractor.__init__(self, adb_manager)
