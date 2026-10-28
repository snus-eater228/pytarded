# game/qr_logic.rpy
# Система снэпшотов для QR-кодов (работает с патчером)

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
    # JSON ЭНКОДЕР/ДЕКОДЕР
    # ==========================================
    class SnapshotEncoder(json.JSONEncoder):
        def default(self, obj):
            class_name = obj.__class__.__name__ if hasattr(obj, '__class__') else ""
            if class_name == "Stat":
                return {"__type__": "Stat", "x": getattr(obj, 'x', 0)}
            if class_name == "LoveVariable":
                return {"__type__": "LoveVariable", "x": getattr(obj, 'x', 0), 
                        "lover": getattr(obj, 'lover', ""), "prev": getattr(obj, "prev", 0.0)}
            return str(obj)

    def reconstruct_object(data):
        if isinstance(data, dict):
            if "__type__" in data:
                obj_type = data["__type__"]
                if obj_type == "Stat":
                    return renpy.store.Stat(x=data.get("x", 0))
                elif obj_type == "LoveVariable":
                    return renpy.store.LoveVariable(x=data.get("x", 0), lover=data.get("lover", ""), prev=data.get("prev", 0.0))
            return {k: reconstruct_object(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [reconstruct_object(item) for item in data]
        return data

    # ==========================================
    # СБОР ПЕРЕМЕННЫХ
    # ==========================================
    def get_serializable_store_vars():
        BLACKLIST = {
            "chapters", "inpval", "persistent", "saved_renpy_keymap",
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
            "_original_config_show", "_character_base_at_list", "latest_snapshot_qr",
            "current_checkpoint", "current_label"
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

    # ==========================================
    # СОЗДАНИЕ СНЭПШОТА
    # ==========================================
    def make_snapshot_debug():
        try:
            current_label = store.current_label
            
            # Сохраняем текущие позиции перед созданием снимка
            save_character_positions()
            
            chars_data = []
            for tag in renpy.get_showing_tags(layer='master'):
                attrs = renpy.get_attributes(tag)
                
                # Получаем сохраненные позиции
                positions = getattr(store, '_saved_character_positions', {}).get(tag, {})
                
                chars_data.append({
                    "t": tag, 
                    "a": [str(a) for a in attrs],
                    "p": positions  # ← Теперь это словарь с координатами
                })
                    
            all_chars = getattr(store, 'ALL_CHARACTERS', ["lars", "james", "kirk", "dave", "nick", "larsroom"])
            bg = "black"
            for tag in renpy.get_showing_tags(layer='master'):
                if tag not in all_chars:
                    bg = tag
                    break

            snapshot = {
                "f": 1,
                "g": "pytarded",
                "cp": current_label,
                "lbl": current_label,
                "bg": bg,
                "c": chars_data,
                "d": get_serializable_store_vars()
            }

            renpy.log("=== DEBUG SNAPSHOT DATA ===\n" + json.dumps(snapshot, indent=2, ensure_ascii=False, cls=SnapshotEncoder) + "\n===========================")

            compact_json = json.dumps(snapshot, separators=(',', ':'), ensure_ascii=False, cls=SnapshotEncoder)
            compressed = zlib.compress(compact_json.encode('utf-8'), 9)
            return base64.b64encode(compressed).decode('ascii')
        except renpy.game.JumpException:
            raise
        except Exception as e:
            renpy.error(f"Snapshot generation failed: {e}")
            import traceback
            traceback.print_exc()
            return None
    def save_character_positions():
        """Сохраняет текущие позиции всех персонажей в store."""
        positions = {}
        
        for tag in renpy.get_showing_tags(layer='master'):
            if tag in ALL_CHARACTERS:
                # Получаем текущий transform персонажа
                displayable = renpy.game.context().scene_lists.get_displayable_by_tag('master', tag)
                if displayable:
                    # Извлекаем позицию из transform
                    # Ren'Py хранит позиции в атрибутах transform
                    transform_info = getattr(displayable, 'transform', None)
                    if transform_info:
                        positions[tag] = {
                            'xpos': getattr(transform_info, 'xpos', 0.5),
                            'ypos': getattr(transform_info, 'ypos', 1.0),
                            'xanchor': getattr(transform_info, 'xanchor', 0.5),
                            'yanchor': getattr(transform_info, 'yanchor', 1.0),
                        }
        
        # Сохраняем в store
        store._saved_character_positions = positions
        #print(f"💾 [POS] Сохранены позиции: {positions}")

    def restore_visuals_from_snapshot(snap):
        """Восстанавливает фон, персонажей и свет из снимка."""
        try:
            print("🎨 [VISUAL] Начинаем восстановление визуала...")
            
            # 1. Восстанавливаем фон
            bg = snap.get("bg", "black")
            print(f"🎨 [VISUAL] Фон: {bg}")
            if bg and bg != "black":
                renpy.scene(bg)
            
            # 2. Восстанавливаем свет
            current_light = snap.get("d", {}).get("current_light")
            if current_light and isinstance(current_light, str):
                print(f"🎨 [VISUAL] Свет: {current_light}")
                if hasattr(renpy.store, 'LightVariable'):
                    setattr(renpy.store, 'current_light', renpy.store.LightVariable(initial_value=current_light))
            
            # 3. Восстанавливаем персонажей с точными координатами
            chars = snap.get("c", [])
            print(f"🎨 [VISUAL] Персонажей в снимке: {len(chars)}")
            
            for char_data in chars:
                tag = char_data.get("t")
                attrs = char_data.get("a", [])
                pos_data = char_data.get("p", {})  # ← Словарь с координатами
                
                if not tag:
                    continue
                
                name = f"{tag} {' '.join(attrs)}" if attrs else tag
                print(f"🎨 [VISUAL] Показываем: {name}, координаты: {pos_data}")
                
                # Создаем Transform с точными координатами
                if pos_data:
                    xpos = pos_data.get('xpos', 0.5)
                    ypos = pos_data.get('ypos', 1.0)
                    xanchor = pos_data.get('xanchor', 0.5)
                    yanchor = pos_data.get('yanchor', 1.0)
                    
                    # Создаем кастомный трансформ с позицией
                    custom_transform = Transform(xpos=xpos, ypos=ypos, xanchor=xanchor, yanchor=yanchor)
                    
                    renpy.show(name, at_list=[custom_transform], layer='master')
                else:
                    renpy.show(name, layer='master')
            
            renpy.with_statement(None)
            print("✅ [VISUAL] Визуал восстановлен")
            
        except Exception as e:
            renpy.error(f"Visual restore failed: {e}")
            import traceback
            traceback.print_exc()
    def restore_variables(vars_data):
        """Восстанавливает переменные из словаря."""
        for key, value in vars_data.items():
            if key == "current_light" and isinstance(value, str):
                setattr(renpy.store, key, renpy.store.LightVariable(initial_value=value))
            else:
                setattr(renpy.store, key, reconstruct_object(value))

    def load_snapshot_from_qr(qr_data):
        """Распаковывает QR, восстанавливает состояние и прыгает на checkpoint-метку."""
        try:
            compressed = base64.b64decode(qr_data)
            json_str = zlib.decompress(compressed).decode('utf-8')
            snap = json.loads(json_str)

            if snap.get("g") != "pytarded" or snap.get("f") != 1:
                renpy.notify("Несовместимая версия сохранения!")
                return

            print("=" * 60)
            print("🔄 [LOAD] Начинаем загрузку снимка...")
            print("=" * 60)

            # 1. Восстанавливаем переменные
            restore_variables(snap.get("d", {}))
            print("✅ [LOAD] Переменные восстановлены")

            # 2. Восстанавливаем визуал (фон, персонажи, свет)
            restore_visuals_from_snapshot(snap)
            print("✅ [LOAD] Визуал восстановлен")

            # 3. Прыгаем на checkpoint-метку
            cp_id = snap.get("cp", "start")
            
            if renpy.has_label(cp_id):
                print(f"🎯 [LOAD] Прыгаем на метку: {cp_id}")
                renpy.jump(cp_id)
            else:
                renpy.notify(f"Метка '{cp_id}' не найдена! Прыгаем на start.")
                renpy.jump("start")
                
        except renpy.game.JumpException:
            raise
        except Exception as e:
            renpy.notify(f"Ошибка чтения QR: {e}")
            import traceback
            traceback.print_exc()

    # ==========================================
    # ИМПОРТ ИЗ JS
    # ==========================================
    def check_snapshot_import_pending():
        """Проверяет файл, созданный JS сканером."""
        if not is_web(): 
            return
        
        marker_path = _save_path("_qr_snapshot_pending")
        
        if os.path.exists(marker_path):
            print("=" * 60)
            print("✅ [IMPORT] ФАЙЛ НАЙДЕН! НАЧИНАЕМ ЗАГРУЗКУ...")
            print("=" * 60)
            try:
                with open(marker_path, "r", encoding="utf-8") as f:
                    qr_data = f.read().strip()
                
                os.unlink(marker_path)
                
                if qr_data:
                    load_snapshot_from_qr(qr_data)
                else:
                    print("⚠️ [IMPORT] Файл был пустым!")
            except renpy.game.JumpException:
                raise
            except Exception as e:
                print(f"❌ [IMPORT] ОШИБКА ЧТЕНИЯ: {e}")
                renpy.error(f"Snapshot import error: {e}")

    config.interact_callbacks.append(check_snapshot_import_pending)

    # ==========================================
    # ИНИЦИАЛИЗАЦИЯ JS
    # ==========================================
    if is_web():
        renpy.emscripten.run_script("""
            setTimeout(() => {
                window.PYTARDED_SAVEDIR = %s;
                console.log("🔗 PYTARDED: Savedir установлен:", window.PYTARDED_SAVEDIR);
                
                if (typeof Module !== 'undefined' && Module.FS) {
                    try {
                        const files = Module.FS.readdir(window.PYTARDED_SAVEDIR);
                        console.log("🔗 PYTARDED JS: Файлы в директории:", files);
                    } catch(e) {
                        console.error("🔗 PYTARDED JS: Ошибка чтения директории:", e);
                    }
                }
            }, 1500);
        """ % json.dumps(renpy.config.savedir))

    # ==========================================
    # ФУНКЦИИ ДЛЯ ЭКРАНОВ
    # ==========================================
    def show_qr_modal():
        """Генерирует снимок и показывает QR."""
        if not is_web():
            renpy.notify("QR работает только в веб-версии")
            return

        qr = make_snapshot_debug()

        if not qr:
            renpy.notify("Не удалось создать снимок.")
            return

        if len(qr) > QR_MAX_CHARS:
            renpy.notify(
                f"ВНИМАНИЕ: Снимок слишком большой ({len(qr)} символов)!\n"
                f"Лимит: {QR_MAX_CHARS}. Посмотри дебаг в логе и вырежь лишние переменные."
            )

        renpy.store.latest_snapshot_qr = qr
        renpy.emscripten.run_script("window.showQRModal(%s);" % json.dumps(qr))

    def show_load_modal():
        """Открывает модалку загрузки."""
        if not is_web():
            renpy.notify("Загрузка работает только в веб-версии")
            return
        renpy.emscripten.run_script("window.openLoadModal && window.openLoadModal();")

    def show_bug_report_modal():
        """Открывает модалку баг-репорта с дампом."""
        if not is_web(): 
            return
        qr = getattr(store, 'latest_snapshot_qr', None) or make_snapshot_debug()
        label = store.current_label
        renpy.emscripten.run_script("window._bugMeta = %s;" % json.dumps({"label": label}))
        renpy.emscripten.run_script("window.openBugModal(%s);" % json.dumps(qr))

        # Авто-сохранение позиций на каждом коллбэке
    def auto_save_positions_label_callback(name, abnormal):
        if not abnormal:
            save_character_positions()

    def auto_save_positions_say_callback(event, interact, **kwargs):
        if event == "begin" and interact:
            save_character_positions()

    config.label_callbacks.append(auto_save_positions_label_callback)
    config.all_character_callbacks.append(auto_save_positions_say_callback)