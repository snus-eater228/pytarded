# game/qr_logic.rpy
# Финальная версия: Динамическая система снэпшотов с корректной обработкой прыжков

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

    def update_current_checkpoint():
        try:
            raw_label = store.current_label
            safe_label = str(raw_label).replace(".", "_").replace("-", "_").replace(" ", "_")
            
            raw_speaker = getattr(store, 'speaking_char', 'narrator')
            safe_speaker = str(raw_speaker).replace(" ", "_").replace(".", "_")
            
            tags = renpy.get_showing_tags(layer='master')
            all_chars = getattr(store, 'ALL_CHARACTERS', ["lars", "james", "kirk", "dave", "nick", "larsroom"])
            
            bg = "black"
            for tag in tags:
                if tag not in all_chars:
                    bg = str(tag)
                    break
            
            store.current_checkpoint = f"{safe_label}_{safe_speaker}_{bg}"
            store.current_label = raw_label
            
        except renpy.game.JumpException:
            raise
        except Exception:
            store.current_checkpoint = "fallback_checkpoint"

    class SnapshotEncoder(json.JSONEncoder):
        def default(self, obj):
            class_name = obj.__class__.__name__ if hasattr(obj, '__class__') else ""
            if class_name == "Stat":
                return {"__type__": "Stat", "x": getattr(obj, 'x', 0)}
            if class_name == "LoveVariable":
                return {"__type__": "LoveVariable", "x": getattr(obj, 'x', 0), "lover": getattr(obj, 'lover', ""), "prev": getattr(obj, "prev", 0.0)}
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
            "_original_config_show", "_character_base_at_list", "latest_snapshot_qr"
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
            update_current_checkpoint()
            final_cp_id = getattr(store, 'current_checkpoint', cp_id)
            
            chars_data = []
            for tag in renpy.get_showing_tags(layer='master'):
                attrs = renpy.get_attributes(tag)
                chars_data.append({"t": tag, "a": [str(a) for a in attrs]})

            all_chars = getattr(store, 'ALL_CHARACTERS', ["lars", "james", "kirk", "dave", "nick", "larsroom"])
            bg = "black"
            for tag in renpy.get_showing_tags(layer='master'):
                if tag not in all_chars:
                    bg = tag
                    break

            snapshot = {
                "f": 1,
                "g": "pytarded",
                "cp": final_cp_id,
                "lbl": store.current_label,
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
            return None

    def show_qr_modal():
        if not is_web():
            renpy.notify("QR работает только в веб-версии")
            return

        cp_id = getattr(renpy.store, 'current_checkpoint', store.current_label)
        qr = make_snapshot_debug(cp_id)

        if not qr:
            renpy.notify("Не удалось создать снимок.")
            return

        renpy.store.latest_snapshot_qr = qr
        renpy.emscripten.run_script("window.showQRModal(%s);" % json.dumps(qr))

    def show_load_modal():
        if not is_web():
            renpy.notify("Загрузка работает только в веб-версии")
            return
        renpy.emscripten.run_script("window.openLoadModal && window.openLoadModal();")

    def show_bug_report_modal():
        if not is_web(): 
            return
        qr = getattr(store, 'latest_snapshot_qr', None) or make_snapshot_debug(getattr(store, 'current_checkpoint', 'start'))
        label = store.current_label
        renpy.emscripten.run_script("window._bugMeta = %s;" % json.dumps({"label": label}))
        renpy.emscripten.run_script("window.openBugModal(%s);" % json.dumps(qr))

    def restore_variables(vars_data):
        for key, value in vars_data.items():
            if key == "current_light" and isinstance(value, str):
                setattr(renpy.store, key, renpy.store.LightVariable(initial_value=value))
            else:
                setattr(renpy.store, key, reconstruct_object(value))

    def update_current_checkpoint():
        try:
            # 1. Получаем РЕАЛЬНЫЙ родительский лейбл (например, "start" или "chapter1")
            raw_label = renpy.game.context().current.label
            
            # 2. Получаем говорящего и фон для уникальности
            raw_speaker = getattr(store, 'speaking_char', 'narrator')
            safe_speaker = str(raw_speaker).replace(" ", "_").replace(".", "_")
            
            tags = renpy.get_showing_tags(layer='master')
            all_chars = getattr(store, 'ALL_CHARACTERS', ["lars", "james", "kirk", "dave", "nick", "larsroom"])
            
            bg = "black"
            for tag in tags:
                if tag not in all_chars:
                    bg = str(tag)
                    break
            safe_bg = str(bg).replace(" ", "_").replace(".", "_")
            
            # 3. СОЗДАЕМ ИМЯ ЛОКАЛЬНОЙ МЕТКИ (без точки в начале для имени переменной)
            local_name = f"{safe_bg}_{safe_speaker}"
            
            # 4. ПОЛНЫЙ АДРЕС МЕТКИ ДЛЯ REN'PY (с точкой!)
            # Например: "start.parking_lars"
            store.current_checkpoint = f"{raw_label}.{local_name}"
            
            # Сохраняем и родительский лейбл для отладки
            store.current_label = raw_label
            
        except renpy.game.JumpException:
            raise
        except Exception:
            store.current_checkpoint = "start.fallback"
            store.current_label = "start"

    def auto_checkpoint_label_callback(name, abnormal):
        if not abnormal:
            update_current_checkpoint()

    def auto_checkpoint_say_callback(event, interact, **kwargs):
        if event == "begin" and interact:
            update_current_checkpoint()

    _fs_diagnostic_done = False

    def check_snapshot_import_pending():
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

    config.label_callbacks.append(auto_checkpoint_label_callback)
    config.all_character_callbacks.append(auto_checkpoint_say_callback)
    config.interact_callbacks.append(check_snapshot_import_pending)

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