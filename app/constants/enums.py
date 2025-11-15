from enum import Enum

class Platform(Enum):
    LINUX = "linux"
    WIN32 = "win32"
    MACOS = "darwin"

class Environment(Enum):
    DEV = "dev"
    STAGING = "staging"
    PROD = "prod"