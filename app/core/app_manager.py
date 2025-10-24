from .app_uninstaller import AppUninstaller
from .app_extractor import AppExtractor
from .app_lister import AppLister

class AppManager(AppLister, AppUninstaller, AppExtractor):
    """Clase principal que combina todas las funcionalidades de gestión de aplicaciones"""
    
    def __init__(self):
        # Llamar al constructor de cada clase padre
        AppLister.__init__(self)
        AppUninstaller.__init__(self) 
        AppExtractor.__init__(self)