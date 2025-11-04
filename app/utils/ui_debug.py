def debug_fill_devices(self, count=10):
    """Rellenar la lista de dispositivos con datos ficticios para pruebas visuales"""
    self.device_list.clear()
    fake_devices = []
    
    for i in range(count):
        device_id = f"emulator-{5554+i}"
        fake_devices.append({
            "brand": f"Marca{i}",
            "model": f"Modelo_{i}",
            "device": device_id
        })
        self.device_list.addItem(f"Marca{i} Modelo_{i} - {device_id}")

def debug_fill_apk_list(self, count=50):
    """Rellenar la lista de APKs con datos ficticios para pruebas visuales"""
    self.selected_apks = [f"/fake/path/app_{i+1}.apk" for i in range(count)]
    self._update_apk_list()
