default current_light = LightVariable()
define ALL_CHARACTERS = ["lars", "james", "kirk", "dave", "nick"]
init python:
    from renpy.display.matrix import Matrix
    
    # Словарь матриц освещения
    lighting_matrices = {
        # Обычный свет - без изменений
        "normal": Matrix((1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0)),
        
        # Розовый - мягкий, не агрессивный
        "pink": Matrix((1.0, 0.3, 0.0, 0.0, 0.0, 0.6, 0.0, 0.0, 0.0, 0.0, 0.9, 0.0, 0.0, 0.0, 0.0, 0.9)),
    
        # Ночь - темнее, но не прозрачный
        "night": Matrix((0.5, 0.0, 0.0, 0.0, 0.0, 0.6, 0.0, 0.0, 0.0, 0.0, 0.85, 0.0, 0.0, 0.0, 0.0, 1.0)),
        
        # Молния - яркий, но не выбеливает
        "lightning": Matrix((1.05, 0.0, 0.0, 0.0, 0.0, 1.05, 0.0, 0.0, 0.0, 0.0, 1.15, 0.0, 0.0, 0.0, 0.0, 1.0)),
        
        # Барби - насыщенный, но мягкий
        "barbie_pink": Matrix((1.15, 0.0, 0.0, 0.0, 0.0, 0.65, 0.0, 0.0, 0.0, 0.0, 1.1, 0.0, 0.0, 0.0, 0.0, 1.0)),
        
        # Ярко-синий - клубный, но не кислотный
        "bright_blue": Matrix((0.65, 0.0, 0.0, 0.0, 0.0, 0.8, 0.0, 0.0, 0.0, 0.0, 1.2, 0.0, 0.0, 0.0, 0.0, 1.0)),
        
        # Солнце - теплый, яркий
        "sunlight": Matrix((1.08, 0.0, 0.0, 0.0, 0.0, 1.05, 0.0, 0.0, 0.0, 0.0, 0.95, 0.0, 0.0, 0.0, 0.0, 1.0)),
        
        # Рассвет - мягкий оранжево-розовый
        "sunrise": Matrix((1.1, 0.0, 0.0, 0.0, 0.0, 0.95, 0.0, 0.0, 0.0, 0.0, 0.85, 0.0, 0.0, 0.0, 0.0, 1.0)),
        
        # Закат - глубокий, но не грязный
        "sunset": Matrix((1.15, 0.0, 0.0, 0.0, 0.0, 0.8, 0.0, 0.0, 0.0, 0.0, 0.9, 0.0, 0.0, 0.0, 0.0, 1.0)),
        
        # Зеленые лампы - матричный, но не ядовитый
        "green_lamps": Matrix((0.6, 0.0, 0.0, 0.0, 0.0, 1.1, 0.0, 0.0, 0.0, 0.0, 0.7, 0.0, 0.0, 0.0, 0.0, 1.0)),
        
        # Теплый ночник - тусклый, уютный
        "warm_nightlight": Matrix((0.85, 0.0, 0.0, 0.0, 0.0, 0.8, 0.0, 0.0, 0.0, 0.0, 0.6, 0.0, 0.0, 0.0, 0.0, 1.0)),
        
        # Розовый ночник - мягкий, нежный
        "pink_nightlight": Matrix((0.95, 0.0, 0.0, 0.0, 0.0, 0.75, 0.0, 0.0, 0.0, 0.0, 0.9, 0.0, 0.0, 0.0, 0.0, 1.0)),
        
        "classroom_cold": Matrix((0.9, 0.0, 0.0, 0.0, 0.0, 1.05, 0.0, 0.0, 0.0, 0.0, 1.1, 0.0, 0.0, 0.0, 0.0, 1.0)),
    
        # Старый класс школы - теплый, приглушенный, желтоватый
        "classroom_old": Matrix((1.05, 0.0, 0.0, 0.0, 0.0, 0.95, 0.0, 0.0, 0.0, 0.0, 0.75, 0.0, 0.0, 0.0, 0.0, 1.0)),
    }
    
    
    class LightVariable:
        """Класс переменной освещения с автоматическим обновлением персонажей"""
        
        def __init__(self, initial_value="normal"):
            self._value = initial_value
        
        @property
        def value(self):
            return self._value
        
        @value.setter
        def value(self, new_value):
            if new_value not in lighting_matrices:
                renpy.error(f"Неизвестное освещение: {new_value}")
                return
            
            self._value = new_value
            
            # Автоматически обновляем всех показанных персонажей
            self._update_all_characters()
            self._update_scene_lighting()
        
        def _update_scene_lighting(self):
            """Автоматически перекрашивает все фоны на сцене"""
            chars = get_showing_characters_and_states()
            
            for tag, attrs in chars.items():
                # Пропускаем персонажей и системные теги
                if tag in ALL_CHARACTERS or tag in ["screensaver", "ui"]:
                    continue
                
                # Проверяем, есть ли у этого тега атрибуты освещения
                # (например, "larsroom" с атрибутом "pink")
                if attrs:
                    # Если фон уже показан с атрибутом освещения, обновляем его
                    new_attrs = list(attrs)
                    # Заменяем старый атрибут освещения на новый
                    # (предполагаем, что атрибут освещения — это последний в списке)
                    if new_attrs and new_attrs[-1] in lighting_matrices:
                        new_attrs[-1] = self._value
                    else:
                        new_attrs.append(self._value)
                    
                    image_name = f"{tag} {' '.join(new_attrs)}"
                    renpy.show(tag, what=image_name)

        def _update_all_characters(self):
            """Перекрашивает всех показанных персонажей с сохранением атрибутов,
            позиций и других трансформов (sprite_highlight и т.д.)."""
            chars = get_showing_characters_and_states()

            for tag, attrs in chars.items():
                if tag not in ALL_CHARACTERS:
                    continue

                displayable = renpy.game.context().scene_lists.get_displayable_by_tag("master", tag)
                if displayable is None:
                    continue

                # Восстанавливаем базовый at_list (позиция + sprite_highlight + ...)
                base_at_list = _character_base_at_list.get(tag, [])

                # НОВОЕ: собираем name = "tag attr1 attr2 ..."
                # (а не what — Ren'Py сам разложит на tag + attrs и найдёт layeredimage)
                if attrs:
                    full_name = f"{tag} {' '.join(attrs)}"
                else:
                    full_name = tag

                atl_transform = getattr(renpy.store, f"lit_{self._value}")

                full_at_list = list(base_at_list) + [atl_transform]

                # ВАЖНО: what=None — Ren'Py ищет по name (правильно для layeredimage)
                # Вызываем _original_config_show напрямую, чтобы не пройти через
                # custom_show повторно (иначе lighting накопится в base_at_list)
                _original_config_show(
                    full_name,        # ← name с атрибутами       # ← ИСПРАВЛЕНО: было what=image_name
                    at_list=full_at_list,
                    zorder=0,
                    layer='master'
                )

            renpy.restart_interaction()
    # Функция для удобной установки (опционально)
    def set_light(lighting_type):
        store.current_light.value = lighting_type
    
    def get_displayed_characters():
        showing_tags = renpy.get_showing_tags(layer='master')
        return list(showing_tags)

init python:
    def get_showing_characters_and_states(layer='master'):
        # Получаем сет всех отображаемых тегов (например, {'eileen', 'bg'})
        showing_tags = renpy.get_showing_tags(layer)
        
        # Собираем словарь, где ключ — тег, а значение — кортеж атрибутов
        result = {}
        for tag in showing_tags:
            attrs = renpy.get_attributes(tag, layer=layer)
            if attrs is not None:
                result[tag] = attrs
            else:
                result[tag] = () # Атрибутов нет (просто картинка без модификаторов)
        return result
# Трансформы для каждого типа освещения
transform lit_normal:
    matrixcolor lighting_matrices["normal"]

transform lit_pink:
    matrixcolor lighting_matrices["pink"]

transform lit_night:
    matrixcolor lighting_matrices["night"]

transform lit_lightning:
    matrixcolor lighting_matrices["lightning"]

transform lit_barbie_pink:
    matrixcolor lighting_matrices["barbie_pink"]

transform lit_bright_blue:
    matrixcolor lighting_matrices["bright_blue"]

transform lit_sunlight:
    matrixcolor lighting_matrices["sunlight"]

transform lit_sunrise:
    matrixcolor lighting_matrices["sunrise"]

transform lit_sunset:
    matrixcolor lighting_matrices["sunset"]

transform lit_green_lamps:
    matrixcolor lighting_matrices["green_lamps"]

transform lit_warm_nightlight:
    matrixcolor lighting_matrices["warm_nightlight"]

transform lit_pink_nightlight:
    matrixcolor lighting_matrices["pink_nightlight"]


init -1 python:
    # Сохраняем оригинальную функцию показа
    _original_config_show = renpy.config.show

    # НОВОЕ: словарь для сохранения базового at_list персонажа (без lighting)
    _character_base_at_list = {}

    def _get_tag(name):
        if isinstance(name, tuple) or isinstance(name, list):
            return name[0]
        return name

    def _get_emotion(name):
        if isinstance(name, tuple):
            if len(name) > 1:
                return name[1]
        elif isinstance(name, str):
            parts = name.split()
            if len(parts) > 1:
                return parts[1]
        return "normal"

    def custom_show(name, what=None, at_list=None, zorder=0, behind=None, layer='master', atl=None, **kwargs):
        tag = _get_tag(name)

        # ==========================================
        # ОБНОВЛЕНИЕ ЭМОЦИИ ДЛЯ FACETIME
        # ==========================================
        if getattr(store, 'is_facetime', False) and tag == getattr(store, 'facetime_caller', ''):
            # Просто обновляем эмоцию для facetime_screen
            emotion = _get_emotion(name)
            if not emotion and what and isinstance(what, str):
                parts = what.split()
                if len(parts) > 1:
                    emotion = parts[1]
            if not emotion:
                emotion = "normal"
            store.facetime_emotion = emotion
            renpy.restart_interaction()
            return
        if store.is_facetime and tag == store.facetime_caller:
            emotion = _get_emotion(name)
            if not emotion and what and isinstance(what, str):
                parts = what.split()
                if len(parts) > 1:
                    emotion = parts[1]
            if not emotion:
                emotion = "normal"
            store.facetime_emotion = emotion
            renpy.restart_interaction()
            
        if tag in ALL_CHARACTERS:
            # НОВОЕ: если at_list не задан — используем ПРЕДЫДУЩИЙ base_at_list,
            # чтобы позиция/подсветка сохранялись между show без явного `at`
            if at_list is None:
                flat_at_list = list(_character_base_at_list.get(tag, []))
                # _character_base_at_list НЕ обновляем — берём как есть
            else:
                # Сплющиваем новый at_list
                flat_at_list = []
                for item in at_list:
                    if isinstance(item, (list, tuple)):
                        flat_at_list.extend(item)
                    else:
                        flat_at_list.append(item)
                # Запоминаем новый base
                _character_base_at_list[tag] = list(flat_at_list)

            # Добавляем lighting в конец
            lighting_transform = getattr(
                renpy.store,
                f"lit_{store.current_light.value}",
                None
            )
            if lighting_transform:
                flat_at_list.append(lighting_transform)
                at_list = flat_at_list

        _original_config_show(name, what=what, at_list=at_list, zorder=zorder, behind=behind, layer=layer, atl=atl, **kwargs)

    renpy.config.show = custom_show