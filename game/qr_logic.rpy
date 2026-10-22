init python:
    import json
    import base64
    import zlib
    
    def show_bug_report_modal():
        """Открывает модалку баг-репорта"""
        label = store.current_label
        runtime = renpy.get_game_runtime()
        
        # Вызываем JS функцию
        js_code = "window.openBugReportModal('%s', %f)" % (label, runtime)
        renpy.emscripten.run_script(js_code)
    
    def show_qr_modal():
        """Экспортирует состояние и открывает модалку с QR"""
        # 1. Сохраняем текущее состояние
        temp_slot = "999"
        renpy.save(temp_slot, "QR Export")
        
        # 2. Получаем данные
        save_data = renpy.get_save(temp_slot)
        
        # 3. Удаляем скриншот (он слишком большой)
        if 'thumbnail' in save_data:
            del save_data['thumbnail']
        
        # 4. Сериализуем минимальные данные
        minimal_data = {
            "v": 1,
            "slot": save_data.get('slot', 1),
            "name": save_data.get('name', 'Export'),
            "data": save_data
        }
        
        # 5. Сжимаем
        json_str = json.dumps(minimal_data, separators=(',', ':'))
        compressed = zlib.compress(json_str.encode('utf-8'), 9)
        encoded = base64.b64encode(compressed).decode('ascii')
        
        # 6. Проверяем размер
        if len(encoded) > 2800:
            renpy.notify("Сохранение слишком большое для QR. Максимум ~2.8KB.")
            renpy.unlink_save(temp_slot)
            return
        
        # 7. Удаляем временное сохранение
        renpy.unlink_save(temp_slot)
        
        # 8. Открываем модалку с QR
        js_code = "window.showQRModal('%s')" % encoded
        renpy.emscripten.run_script(js_code)
    
    def import_save_from_js(encoded_data):
        """Импортирует сохранение из JS"""
        try:
            # Декодируем и распаковываем
            compressed = base64.b64decode(encoded_data)
            json_str = zlib.decompress(compressed).decode('utf-8')
            data = json.loads(json_str)
            
            # Здесь нужно восстановить сохранение
            # Это сложная часть - требует работы с внутренним API
            renpy.notify("Импорт сохранений пока в разработке")
            
        except Exception as e:
            renpy.notify(f"Ошибка импорта: {e}")