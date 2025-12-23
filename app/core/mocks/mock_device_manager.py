import hashlib
import random
import string
from app.data.mock_catalogs import BRANDS, MANUFACTURERS, RESOLUTIONS, CPU_ARCHS


class MockDeviceManager:
    """
    DeviceManager ficticio para documentación, demos y UI preview.
    NO usa ADB.
    NO contiene datos reales.
    """

    def __init__(self):
        # --------------------------------------------------
        # Catalogos importados desde mock_catalogs.py
        # --------------------------------------------------
        self._brands = BRANDS
        self._manufacturers = MANUFACTURERS
        self._resolutions = RESOLUTIONS
        self._cpu_archs = CPU_ARCHS

        # --------------------------------------------------
        # Dispositivos (device_id == serial)
        # --------------------------------------------------
        self._devices = [
            {"device": self._generate_serial(i), "status": "device"}
            for i in range(1, 11)
        ]

        # Enriquecer lista con modelo y marca coherentes
        for d in self._devices:
            profile = self._generate_profile(d["device"])
            d.update({
                "model": profile["model"],
                "brand": profile["brand"]
            })

    # --------------------------------------------------
    # Serial alfanumérico realista (device_id == serial)
    # --------------------------------------------------
    def _generate_serial(self, index):
        rnd = random.Random(index)
        suffix = "".join(rnd.choices(string.ascii_uppercase + string.digits, k=8))
        return f"SN{index:02d}{suffix}"

    # --------------------------------------------------
    # Modelo: 3–4 caracteres, variados y legibles
    # --------------------------------------------------
    def _generate_model_code(self, rnd):
        letters = "ABCDEFGHJKLMNPQRSTUVWYZ"

        patterns = [
            lambda: f"{rnd.choice(letters)}{rnd.randint(1,9)}{rnd.choice(letters)}",
            lambda: f"{rnd.choice(letters)}{rnd.choice(letters)}{rnd.randint(1,9)}",
            lambda: f"{rnd.choice(letters)}{rnd.randint(10,99)}",
            lambda: f"{rnd.choice(letters)}{rnd.choice(letters)}{rnd.randint(10,99)}",
        ]

        return rnd.choice(patterns)()

    # --------------------------------------------------
    # Perfil determinístico por serial
    # --------------------------------------------------
    def _generate_profile(self, device_id):
        seed = int(hashlib.md5(device_id.encode()).hexdigest(), 16)
        rnd = random.Random(seed)

        return {
            "model": self._generate_model_code(rnd),
            "brand": rnd.choice(self._brands),
            "manufacturer": rnd.choice(self._manufacturers),
            "android_version": f"{rnd.randint(11, 15)}.{rnd.randint(0, 4)}",
            "sdk_version": str(rnd.randint(30, 39)),
            "resolution": rnd.choice(self._resolutions),
            "density": f"{rnd.choice([420, 480, 520])} dpi",
            "total_ram": f"{rnd.choice([4096, 8192, 12288, 16384])} MB",
            "storage": f"{rnd.choice([64, 128, 256, 512])} GB",
            "cpu_arch": rnd.choice(self._cpu_archs),
        }

    # --------------------------------------------------
    # Lista de dispositivos
    # --------------------------------------------------
    def get_connected_devices(self):
        return {
            "success": True,
            "devices": self._devices,
            "message": f"Se encontraron {len(self._devices)} dispositivos (mock)"
        }

    # --------------------------------------------------
    # Información de UN dispositivo
    # --------------------------------------------------
    def get_device_info(self, device_id):
        if not self.is_device_available(device_id):
            return {
                "success": False,
                "message": "Dispositivo no encontrado (mock)"
            }

        profile = self._generate_profile(device_id)

        return {
            "success": True,
            "device_id": device_id,
            "serial_number": device_id,
            **profile
        }

    # --------------------------------------------------
    # Disponibilidad
    # --------------------------------------------------
    def is_device_available(self, device_id):
        return any(d["device"] == device_id for d in self._devices)
