import sys
from app.constants.enums import Platform

print("Inicializando plataforma...")
PLATFORM = Platform(sys.platform)
