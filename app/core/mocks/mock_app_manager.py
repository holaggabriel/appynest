import hashlib
import random
from app.data.mock_catalogs import BRANDS, APP_NAMES, SYSTEM_APPS

class MockAppManager:
    def __init__(self):
        self._brands = BRANDS
        self._app_names = APP_NAMES
        self._system_apps = SYSTEM_APPS

    def get_installed_apps_by_type(self, device_id, device_brand, app_type="all"):
        rnd = self._seed_from_device(device_id)
        target_count = rnd.randint(8, 16)
        apps = []
        seen_names = set()

        max_attempts = target_count * 4
        attempts = 0

        while len(apps) < target_count and attempts < max_attempts:
            attempts += 1
            app = self._generate_app(rnd, device_brand)

            if app_type == "system" and not app["is_system"]:
                continue
            if app_type == "user" and app["is_system"]:
                continue
            if app["name"] in seen_names:
                continue

            seen_names.add(app["name"])
            apps.append(app)

        apps.sort(key=lambda x: x["name"].lower())

        return {
            "success": True,
            "message": f"Se obtuvieron {len(apps)} aplicaciones (mock)",
            "data": {"apps": apps}
        }

    def _generate_app(self, rnd, device_brand):
        name = rnd.choice(self._app_names)
        is_system = name in self._system_apps
        package_name = f"com.{device_brand.lower()}.{name.lower()}"
        version = f"{rnd.randint(1,5)}.{rnd.randint(0,9)}.{rnd.randint(0,9)}"
        apk_path = (
            f"/system/app/{name}/{name}.apk"
            if is_system
            else f"/data/app/{package_name}-{rnd.randint(100,999)}/base.apk"
        )

        return {
            "package_name": package_name,
            "name": name,
            "version": version,
            "apk_path": apk_path,
            "is_system": is_system,
        }

    def _seed_from_device(self, device_id):
        seed = int(hashlib.md5(device_id.encode()).hexdigest(), 16)
        return random.Random(seed)
