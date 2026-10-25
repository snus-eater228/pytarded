# game/qr_logic.rpy
# Система снэпшотов с АВТОМАТИЧЕСКИМ обновлением чекпоинтов и корректной загрузкой

init python:
    import json
    import zlib
    import base64
    import os

    QR_MAX_CHARS = 2400 
    
    def is_web():
        return renpy.emscripten is not None

    def _save_path(filename):
        return os.path.join(renpy.config.savedir, filename)

    # ==========================================
    # 1. АВТОМАТИЧЕСКАЯ ГЕНЕРАЦИЯ ЧЕКПОИНТА
    # ==========================================
    def update_current_checkpoint():
        """
        Автоматически обновляет store.current_checkpoint при смене 
        лейбла, говорящего или сцены.
        """
        try:
            # 1. Текущий лейбл (очищаем от недопустимых символов для имен меток)
            raw_label = renpy.game.context().current.label
            safe_label = str(raw_label).replace(".", "_").replace("-", "_").replace(" ", "_")
            
            # 2. Текущий говорящий (из твоего дампа мы знаем, что есть store.speaking_char)
            raw_speaker = getattr(store, 'speaking_char', 'narrator')
            safe_speaker = str(raw_speaker).replace(" ", "_").replace(".", "_")
            
            # 3. Текущий фон (первый тег на слое master, который НЕ является персонажем)
            # Мы НЕ используем get_scene_lists, мы используем безопасный get_showing_tags
            tags = renpy.get_showing_tags(layer='master')
            all_chars = getattr(store, 'ALL_CHARACTERS', ["lars", "james", "kirk", "dave", "nick", "larsroom"])
            
            bg = "unknown_bg"
            for tag in tags:
                # Ищем первый тег, которого нет в списке персонажей (это и есть фон)
                if tag not in all_chars:
                    bg = str(tag).replace(" ", "_").replace(".", "_")
                    break
            
            # Собираем уникальный ID чекпоинта
            store.current_checkpoint = f"{safe_label}_{safe_speaker}_{bg}"
            
        except Exception as e:
            # Фоллбэк на случай ошибки, чтобы игра не крашнулась
            store.current_checkpoint = "fallback_checkpoint"

    # ==========================================
    # 2. КАСТОМНЫЙ JSON-ЭНКОДЕР И ДЕКОДЕР
    # ==========================================
    class SnapshotEncoder(json.JSONEncoder):
        def default(self, obj):
            class_name = obj.__class__.__name__ if hasattr(obj, '__class__') else ""
            if class_name == "Stat":
                return {"__type__": "Stat", "x": getattr(obj, 'x', 0)}
            if class_name == "LoveVariable":
                return {
                    "__type__": "LoveVariable", 
                    "x": getattr(obj, 'x', 0), 
                    "lover": getattr(obj, 'lover', ""),
                    "prev": getattr(obj, "prev", 0.0)
                }
            return str(obj)

    def reconstruct_object(data):
        """Превращает словари с __type__ обратно в объекты Ren'Py"""
        if isinstance(data, dict):
            if "__type__" in data:
                obj_type = data["__type__"]
                if obj_type == "Stat":
                    return renpy.store.Stat(x=data.get("x", 0))
                elif obj_type == "LoveVariable":
                    return renpy.store.LoveVariable(
                        x=data.get("x", 0), 
                        lover=data.get("lover", ""), 
                        prev=data.get("prev", 0.0)
                    )
            return {k: reconstruct_object(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [reconstruct_object(item) for item in data]
        return data

    # ==========================================
    # 3. СБОР ДАННЫХ
    # ==========================================
    def get_serializable_store_vars():
        BLACKLIST = {
            "chapters", "inpval", "persistent", "current_label", "saved_renpy_keymap",
            "PY2", "main_menu", "mouse_visible", "suppress_overlay", "save_name", 
            "nvl_list", "is_hovered", "is_opened", "is_selected", "quick_menu", 
            "speaking_char", "say_window_show_transform", "nvl_mode",
            "snus", "bell", "barabere", "glass", "PHONK_RADIO_URL",
            "vk_blue", "vk_bg", "vk_block", "vk_text", "vk_text_gray", "vk_link",
            "james_zoom__koef", "dave_zoom_koef", "lars_zoom__koef", 
            "kirk_zoom_koef", "nick_zoom__koef", "girl_zoom_koef", "sprite_focus",
            "adjusted_bounce_path", "lighting_matrices", "PathInterpolator", 
            "PathMotion", "clamp", "calculate_trajectory", "ALL_CHARACTERS", "QR_MAX_CHARS",
            "lit_normal", "lit_pink", "lit_night", "lit_lightning", "lit_barbie_pink", 
            "lit_bright_blue", "lit_sunlight", "lit_sunrise", "lit_sunset", 
            "lit_green_lamps", "lit_warm_nightlight", "lit_pink_nightlight",
            "_original_config_show", "_character_base_at_list"
        }
        
        vars_dict = {}
        for key, value in vars(renpy.store).items():
            if key.startswith('_') or callable(value) or key in BLACKLIST:
                continue
            
            class_name = value.__class__.__name__ if hasattr(value, '__class__') else ""
            
            if class_name == "LightVariable":
                vars_dict[key] = value.value
                continue
            
            if class_name in ("Stat", "LoveVariable"):
                vars_dict[key] = value
                continue

            if isinstance(value, (int, float, str, bool, list, dict)):
                if isinstance(value, (list, dict)) and len(str(value)) > 2000:
                    continue
                vars_dict[key] = value
                
        return vars_dict

    def make_snapshot_debug(cp_id):
        try:
            # Принудительно обновляем чекпоинт прямо перед созданием снимка, 
            # на случай если коллбэк не сработал
            update_current_checkpoint()
            final_cp_id = getattr(store, 'current_checkpoint', cp_id)
            
            chars_data = []
            for tag in renpy.get_showing_tags(layer='master'):
                attrs = renpy.get_attributes(tag)
                chars_data.append({"t": tag, "a": [str(a) for a in attrs]})

            store_vars = get_serializable_store_vars()

            snapshot = {
                "f": 1,
                "g": "pytarded",
                "cp": final_cp_id,
                "lbl": renpy.game.context().current.label,
                "c": chars_data,
                "d": store_vars
            }

            pretty_json = json.dumps(snapshot, indent=2, ensure_ascii=False, cls=SnapshotEncoder)
            renpy.log("=== DEBUG SNAPSHOT DATA ===\n" + pretty_json + "\n===========================")

            compact_json = json.dumps(snapshot, separators=(',', ':'), ensure_ascii=False, cls=SnapshotEncoder)
            compressed = zlib.compress(compact_json.encode('utf-8'), 9)
            return base64.b64encode(compressed).decode('ascii')

        except Exception as e:
            renpy.error(f"Snapshot generation failed: {e}")
            return None

    # ==========================================
    # 4. ФУНКЦИИ ДЛЯ ЭКРАНОВ
    # ==========================================
    def show_qr_modal():
        if not is_web():
            renpy.notify("QR работает только в веб-версии")
            return

        cp_id = getattr(store, 'current_checkpoint', 'start')
        qr = make_snapshot_debug(cp_id)

        if not qr:
            renpy.notify("Не удалось создать снимок.")
            return

        if len(qr) > QR_MAX_CHARS:
            renpy.notify(f"Снимок слишком большой ({len(qr)} символов)! Лимит: {QR_MAX_CHARS}.")
            # Не делаем return, чтобы ты могла протестировать

        store.latest_snapshot_qr = qr
        renpy.emscripten.run_script("window.showQRModal(%s);" % json.dumps(qr))

    def show_load_modal():
        if not is_web():
            renpy.notify("Загрузка работает только в веб-версии")
            return
        renpy.emscripten.run_script("window.openLoadModal && window.openLoadModal();")

    def show_bug_report_modal():
        if not is_web():
            renpy.notify("Баг-репорт работает только в веб-версии")
            return

        qr = getattr(store, 'latest_snapshot_qr', None)
        if not qr:
            qr = make_snapshot_debug(getattr(store, 'current_checkpoint', 'start'))

        label = renpy.game.context().current.label
        runtime = 0.0
        try:
            runtime = float(renpy.get_game_runtime())
        except:
            pass

        renpy.emscripten.run_script("window._bugMeta = %s;" % json.dumps({"label": label, "runtime": runtime}))
        renpy.emscripten.run_script("window.openBugModal(%s);" % json.dumps(qr))

    # ==========================================
    # 5. ЗАГРУЗКА И ВОССТАНОВЛЕНИЕ
    # ==========================================
    def restore_variables(vars_data):
        for key, value in vars_data.items():
            if key == "current_light" and isinstance(value, str):
                setattr(renpy.store, key, renpy.store.LightVariable(initial_value=value))
            else:
                setattr(renpy.store, key, reconstruct_object(value))

    def load_snapshot_from_qr(qr_data):
        try:
            compressed = base64.b64decode(qr_data)
            json_str = zlib.decompress(compressed).decode('utf-8')
            snap = json.loads(json_str)

            if snap.get("g") != "pytarded" or snap.get("f") != 1:
                renpy.notify("Несовместимая версия сохранения!")
                return

            restore_variables(snap.get("d", {}))

            cp_id = snap.get("cp", "start")
            restore_label = "restore_" + cp_id
            
            # ВАЖНО: renpy.jump() из interact_callback корректно передает управление.
            # Но чтобы убедиться, что экран перерисуется, мы можем добавить 
            # неявный restart_interaction внутри самой метки restore_ в script.rpy
            
            if renpy.has_label(restore_label):
                renpy.jump(restore_label)
            else:
                renpy.notify(f"Метка '{restore_label}' не найдена! Возврат в начало.")
                renpy.jump("start")

        except Exception as e:
            renpy.notify(f"Ошибка чтения QR: {e}")

    # ==========================================
    # 6. КОЛЛБЭКИ ДЛЯ АВТО-ОБНОВЛЕНИЯ И ИМПОРТА
    # ==========================================
    def auto_checkpoint_label_callback(name, abnormal):
        if not abnormal:
            update_current_checkpoint()

    def auto_checkpoint_say_callback(event, interact, who, what, kwargs):
        if event == "begin" and interact:
            update_current_checkpoint()

    def check_snapshot_import_pending():
        if not is_web():
            return
        
        marker_path = _save_path("_qr_snapshot_pending")
        if os.path.exists(marker_path):
            try:
                with open(marker_path, "r", encoding="utf-8") as f:
                    qr_data = f.read().strip()
                os.unlink(marker_path)
                if qr_data:
                    load_snapshot_from_qr(qr_data)
            except Exception as e:
                renpy.error(f"Snapshot import error: {e}")

    # Регистрируем ВСЕ коллбэки
    config.label_callback = auto_checkpoint_label_callback
    config.say_callback = auto_checkpoint_say_callback
    config.interact_callbacks.append(check_snapshot_import_pending)

    # Инициализация JS переменной
    if is_web():
        renpy.emscripten.run_script("""
            setTimeout(() => {
                window.PYTARDED_SAVEDIR = %s;
                console.log("🔗 PYTARDED: Savedir установлен в:", window.PYTARDED_SAVEDIR);
            }, 1000);
        """ % json.dumps(renpy.config.savedir))