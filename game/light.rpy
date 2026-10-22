default current_light = LightVariable()
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
    
    # Список всех персонажей (добавь своих)
    ALL_CHARACTERS = ["lars", "james", "kirk", "dave", "nick"]
    
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
            """Перекрашивает всех показанных персонажей с сохранением атрибутов и позиций"""
            
            chars = get_showing_characters_and_states()
            
            for tag, attrs in chars.items():
                if tag not in ALL_CHARACTERS:
                    continue
                
                # Получаем текущий displayable (включая трансформы)
                displayable = renpy.game.context().scene_lists.get_displayable_by_tag("master", tag)
                
                if displayable is None:
                    continue
                
                # Создаем имя изображения с атрибутами
                if attrs:
                    image_name = f"{tag} {' '.join(attrs)}"
                else:
                    image_name = tag
                
                # Показываем с новым освещением
                # Ren'Py автоматически применит матрицу через трансформ lit_{value}
                atl_transform = getattr(renpy.store, f"lit_{self._value}")
                renpy.show(tag, what=image_name, at_list=[atl_transform])
            
        
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
    
    def _get_tag(name):
        """Безопасно извлекает тег (строка или кортеж)"""
        if isinstance(name, tuple) or isinstance(name, list):
            return name[0]
        return name

    def _get_emotion(name):
        """Извлекает эмоцию из name (может быть строкой или кортежем)"""
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
        if store.is_facetime and tag == store.facetime_caller:
            # Пытаемся получить эмоцию из разных источников
            emotion = None
            
            # 1. Проверяем name (может быть кортежем ("james", "sad"))
            emotion = _get_emotion(name)
            
            # 2. Если не нашли, проверяем what
            if not emotion and what and isinstance(what, str):
                parts = what.split()
                if len(parts) > 1:
                    emotion = parts[1]
            
            # 3. Если все еще нет, сбрасываем на normal
            if not emotion:
                emotion = "normal"
            
            # Обновляем переменную
            store.facetime_emotion = emotion
            
            # Перерисовываем экран телефона
            renpy.restart_interaction()
            return
        if tag in ALL_CHARACTERS:
            # Получаем объект трансформации освещения
            lighting_transform = getattr(
                renpy.store, 
                f"lit_{store.current_light.value}", 
                None
            )
            
            if lighting_transform:
                # 1. Сплющиваем (flatten) существующий at_list, чтобы убрать вложенные списки
                flat_at_list = []
                if at_list:
                    for item in at_list:
                        if isinstance(item, (list, tuple)):
                            flat_at_list.extend(item)
                        else:
                            flat_at_list.append(item)
                
                # 2. Добавляем наше освещение в конец плоского списка
                flat_at_list.append(lighting_transform)
                at_list = flat_at_list
        
        _original_config_show(name, what=what, at_list=at_list, zorder=zorder, behind=behind, layer=layer, atl=atl, **kwargs)
    
    renpy.config.show = custom_show