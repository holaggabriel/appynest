import os
import sys
from app.constants.enums import Environment, Platform

APP_NAME = "Appy Nest"
APP_VERSION = "1.0.0"
ORGANIZATION_NAME = "holaggabriel"
ORGANIZATION_DOMAIN = "appynest.dev"
APP_REPOSITORY_URL="https://github.com/holaggabriel/appynest"
APP_ID = "holaggabriel.appynest"
FORM_URL = "https://forms.gle/LFJCeutHFTiYwAHt8"
DONATION_URL = "https://buymeacoffee.com/appynest"
APP_TUTORIAL_URL = "https://www.youtube.com/@random.information.random"
PACKAGE_NAME = "appynest" # Nombre que va a tener el paquete generado, ya sea .exe o .appimage
CONFIG_DIR_NAME = ".appynest"
CONFIG_FILE_NAME = "config.json"

ENVIRONMENT = Environment(os.getenv("ENV", "prod"))
DEBUG_MODE = ENVIRONMENT != "prod"

PLATFORM = Platform(sys.platform)