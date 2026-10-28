# ==========================================
# 1. ПЕРЕМЕННЫЕ СОСТОЯНИЯ
# ==========================================
default liked_post = False
default sixseven_played = False 
default radio_playing = False
default idle_timer = 0  # Твой надежный таймер неактивности

# Динамический список комментариев. Изначально пустой или с парой стартовых.
default vk_comments_list = [
    {"name": "ЛаР$$$иК =)", "avatar": "lars_ava", "text": "какая тварь это в интернет выложила???"},
    {"name": "dave-the-methanix", "avatar": "dave_ava", "text": "что блять выложила это фотошоп галимый! не было этого!!"},
    {"name": "NICK'0t1n3 :3", "avatar": "nick_ava", "text": "бля мужики я с вами даже в одном поле срать теперь не сяду"},
    {"name": "dave-the-methanix", "avatar": "dave_ava", "text": "да блять не было этого хватит это форсить"},
    {"name": "киркуша", "avatar": "kirk_ava", "text": "а почему меня не позвали??("},
    {"name": "ЛаР$$$иК =)", "avatar": "lars_ava", "text": "ага ага ботана забыли спросить"},
    {"name": "dave-the-methanix", "avatar": "dave_ava", "text": "сука никто не был в этой блядской сауне ща я у джеймса спрошу он тоже скажет что не был"},
    {"name": "ЛаР$$$иК =)", "avatar": "lars_ava", "text": "а че он не видел еще?))"},
    {"name": "NICK'0t1n3 :3", "avatar": "nick_ava", "text": "вам видимо совсем делать нехер"},
    {"name": "ЛаР$$$иК =)", "avatar": "lars_ava", "text": "ооо он вроде в сети! печатает что-то"},
    {"name": "James H. (Senior Python/C/C++ developer)", "avatar": "james_ava", "text": "У моего соседа - Васи\nБыл огромный толстый член,\nОн рельефно и пикантно\nПростирался до колен;\nВот однажды, выйдя в поле,\nПривязал елду к ноге,\nЧтобы та своим размером\nНе мешала при ходьбе;\nДевок было просто уйма\nУ соседа моего,\nВсем хотелось хоть однажды\nНасадиться на него;\nДа не просто насадиться,\nА коснуться жопой ног,\nНо двадцатка сантиметров\nГлубины их был порог;\nИ тогда, однажды Вася,\nВ руку взяв большой топор,\nРубанул... гуся по шее\nВашим мыслям в перекор;\nНу не станет же мужчина,\nЧья елда аж до колен,\nОтрубать себе причину\nСотрясанья звуком стен 😏\nВот однажды, в Голливуде\nПро соседа услыхав,\nОтослали к нему девок:\nС грудью, жопой и чулках;\nВсе хотелось им проверить:\nНеужели наяву,\nНи один не смог осилить\nЧудо-Васину елду?\nПриезжали на машинах\nСамолетах, катерах,\nПоездами, в лимузинах,\nПароходах, скутерах\nПрилетали вертолетом,\nПорнозвезды, богачи,\nВсем не верилось, что в жизни\nДо колена есть хуи;\nВот настал черед примерки,\nКто же сможет до конца\nОседлать красавца парня\nИ его красно бойца?\nПервой быть американка\nПожелала быть, и сев,\nНе дошла и до двадцатки:\nРаззадорив прочив дев;\nСледом прыгнула немчанка,\nЧлен тот лихо оседлав,\nУглубилась до 2х дюжин,\nКонкурентку обогнав;\nВслед за ней, на хер огромный\nСо стремянки небольшой\nГордо прыгнула японка,\nРаздвигая 'вход' рукой;\nНо, увы, как ни стараясь\nДальше чем пятнадцать дюйм\nТа японка не скользнула\nСо стыдом покинув хуй;\nСтраны пробовали разны:\nИ французы, и хохлы,\nИ испанцы, англичане,\nПортугальцы, поляки;\nНу никто не мог усесться\nНа огромный Васин член,\nКак в толпе вдруг еле слышно\nПрозвучало: можно мне?\nВышла баба неказиста:\nНи лица, ни форм, ни ног\nПодошла к соседу Васе,\nГоворит: готов, милок?\nВася, вдоволь насмотревшись\nНа потуги разных стран\nРавнодушно согласился\nНа попытку сей мадам;\nДама ногу перекинув,\nСарафан свой приподняв,\nОседлала Васю лихо\nЧлен влагалищем обняв;\nИ скользила она быстро,\nВзор людской в момент сковав,\nИ на зависть всем актрисам\nСела, смачный шлеп издав;\nС оглушающими ухо,\nС громом будто при грозе,\nУдарялись в пол жевала:\nЧелюсть била по земле;\nОбалдев от бабаской прыти,\nЕле выжав из себя,\nВася тихим стоном выдал:\nКто же ты такая, а?!\nТетка мягко улыбнувшись,\nЧтобы Васю не смущать,\nОтвечала ему нежно:\nЯ ж, дружок, админа мать)"},
    {"name": "ЛаР$$$иК =)", "avatar": "lars_ava", "text": "0_0 вопрос закрыт"},
]

# ==========================================
# 2. ИНИЦИАЛИЗАЦИЯ И ФУНКЦИИ
# ==========================================
init -1 python:
    renpy.music.register_channel("phonk", mixer="music", loop=True, tight=True)

init python:
    PHONK_RADIO_URL = "https://phonk-radio.snuseater.workers.dev"

    def toggle_phonk_radio():
        store.radio_playing = not store.radio_playing
        if store.radio_playing:
            renpy.open_url(PHONK_RADIO_URL)
            renpy.notify("📻 Радио открыто в браузере!")
        else:
            renpy.notify("📻 Чтобы выключить, закрой вкладку браузера.")

    def radio_status_text():
        return "📻 Радио: ВКЛ" if store.radio_playing else "📻 Радио: ВЫКЛ"

    def play_sixseven_if_liked():
        if store.liked_post and not store.sixseven_played:
            renpy.play("gui/xp_menu/67.ogg", channel="sound")
            store.sixseven_played = True
# ==========================================
# 3. ИЗОБРАЖЕНИЯ И ТРАНСФОРМЫ
# ==========================================
image sign = "gui/sign.png"


# ==========================================
# 4. ЦВЕТОВАЯ ПАЛИТРА
# ==========================================
define vk_blue = "#4a76a8"
define vk_bg = "#edeef0"
define vk_block = "#ffffff"
define vk_text = "#000000"
define vk_text_gray = "#818c99"
define vk_link = "#2a5885"

# ==========================================
# 5. ЭКРАНЫ
# ==========================================

# !!! ИЗМЕНЕН ТОЛЬКО ЭТОТ ЭКРАН ПОД ГОРИЗОНТАЛЬНЫЙ ФОРМАТ !!!
screen social_network_ui():
    # 1. ФОН ВСЕЙ СТРАНИЦЫ
    add Solid(vk_bg) xysize (1.0, 1.0)

    frame:
        background Solid(vk_blue)
        xfill True
        ysize 50
        padding (10, 70, 10, 60)
        yalign 0.0
        
        hbox:
            spacing 30 # Чуть больше воздуха для широкого экрана
            yalign 0.5 
            
            text "сплетник 'п(р)итон' - свежие новости!" color "#ffffff"  font "gui/tahoma.ttf" size 32
            null width 40

            textbutton  "Новости" action NullAction() text_font "gui/tahoma.ttf" text_color "#ffffff"  text_hover_color "#ffffff" text_outlines [(1, "#123f4d", 0, 0)] text_size 30
            textbutton "Друзья" action NullAction() text_color "#b0c4de" text_hover_color "#ffffff" text_size 30 text_font "gui/tahoma.ttf"
            textbutton "Игры" action NullAction() text_color "#b0c4de" text_hover_color "#ffffff" text_size 30 text_font "gui/tahoma.ttf"
            textbutton "Музыка" action NullAction() text_color "#b0c4de" text_hover_color "#ffffff" text_size 30 text_font "gui/tahoma.ttf"
            textbutton "Видео" action NullAction() text_color "#b0c4de" text_hover_color "#ffffff" text_size 30 text_font "gui/tahoma.ttf"
            
            textbutton "Выйти" action Quit() text_color "#92d6e0" text_hover_color "#ffffff" text_size 30 text_font "gui/tahoma.ttf"

    # # 3. ОСНОВНОЙ КОНТЕНТ (Адаптирован под ширину 1200px)
    frame:
        background Null()
        xfill True
        yfill True
        padding (30, 70, 30, 30) # Чуть больше боковые отступы для "воздуха"
        
        hbox:
            spacing 30 # Больше расстояния между колонками
            xfill True
            yfill True

            # --- ЛЕВАЯ КОЛОНКА (АВАТАРКА) ---
            vbox:
                xsize 250 # Расширили для горизонтального формата
                spacing 15

                frame:
                    background Solid(vk_block)
                    padding (20,0)
                    xfill True
                    
                    vbox:
                        spacing 5
                        add "gui/xp_menu/lars_thumbnail.png" xysize (210, 210) # Аватарка чуть крупнее
                        text "ЛаР$$$иК =)" color vk_link size 28 bold True xalign 0.5 font "gui/tahoma.ttf"
                        text "Статус: 'если в твоей жизни ЖОПА - делай ею опа-опа!!))))' (с) Жак Фреско" color "#555555" size 30 text_align 0 font "gui/tahoma.ttf"
                        text "Играет трек🎶: FACE - Я ебал твою тёлку" color "#567486" font "gui/tahoma.ttf" size 24 text_align 0
                        text "В сети 🟢" color "#333" size 26 xalign 0.5 text_align 0 font "gui/tahoma.ttf"

            # --- ПРАВАЯ КОЛОНКА (ПОСТ И КОММЕНТЫ) ---


            frame:
                background Solid(vk_block)
                style "main_menu_font"
                padding (25, 0)
                xysize (750, 420) # Размер видимой области
                
                vbox:
                    xfill True
                    yfill True
                    spacing 15
                    
                    viewport:
                        scrollbars "vertical"
                        mousewheel True
                        draggable True
                        xfill True
                        yfill True
                        
                        vbox:
                            xfill True
                            spacing 15

                            # Шапка поста
                            hbox:
                                spacing 10
                                text "Анонимус" color vk_link size 32 kerning 2.0 bold True font "gui/tahoma.ttf"
                                text "2 часа назад" color vk_text_gray size 20 yalign 0.6 font "gui/tahoma.ttf"

                            # Текст сплетни
                            text "ШОК_КОНТЕНТ! Пьяный скуф Хэтфилд жёстко нашампурил двух альтушек Дэйва и Ларса в сауне!!! Смотреть онлайн без регистрации!" color vk_text size 30 font "gui/tahoma.ttf" text_align 0 
                                        

                            # Видео-обложка
                            fixed:
                                xsize 640
                                ysize 360
                                xalign 0.5
                                
                                add "gui/xp_menu/hamam.jpg" xysize (640, 360)
                                
                                textbutton "▶":
                                    action Show("rickroll")
                                    text_color "#ffffff"
                                    text_hover_color "#cccccc"
                                    text_size 120
                                    xalign 0.5
                                    yalign 0.5
                                    background None
                                    hover_background None

                            # Лайки (теперь внутри viewport, без ypos/xpos)
                            hbox:
                                spacing 15
                                xalign 0.9 # Прижимаем вправо
                                
                                button:
                                    action [
                                        ToggleVariable("liked_post"),
                                        Function(play_sixseven_if_liked)
                                    ]
                                    if liked_post:
                                        text "❤️ 67" font "gui/tahoma.ttf" color "#ff3347" size 28 bold True
                                    else:
                                        text "🤍 66" font "gui/tahoma.ttf" color vk_text_gray size 28 bold True

                                # Текст "Комментарии" (теперь внутри viewport)
                                text "Комментарии" font "gui/tahoma.ttf" color vk_link size 25 kerning 2.0 bold True ypos 10

                            # Разделитель
                            add Solid("#e1e3e6") xysize (1.0, 2)

                            # Комментарии (теперь внутри viewport)
                            for comment in vk_comments_list:
                                hbox:
                                    spacing 15
                                    
                                    add comment["avatar"] xysize (50, 50)
                                    vbox:
                                        xfill True
                                        text comment["name"] font "gui/tahoma.ttf" color vk_link size 30 bold True kerning 2.0 text_align 0.0 xalign 0.0
                                        text comment["text"] font "gui/tahoma.ttf" color vk_text size 28 text_align 0.0 xalign 0.0

# --- ГЛАВНОЕ МЕНЮ (ТВОЙ КОД БЕЗ ИЗМЕНЕНИЙ) ---
screen xp_main_menu():
    tag menu
    modal True

    add "gui/xp_menu/bg.jpeg" xysize(1920, 1080)

    # Таймер неактивности (стандартный и надежный способ в Ren'Py)
    timer 1.0 action IncrementVariable("idle_timer") repeat True
    
    # Если бездействие >= 60 секунд, сбрасываем таймер и показываем скринсейвер
    if idle_timer >= 60:
        timer 0.1 action [SetVariable("idle_timer", 0), Show("screensaver")]

    # Ярлыки
    vbox:
        xalign 0.02
        yalign 0.15

        imagebutton:
            xpos 50
            idle "play"
            hover "play_hover"
            action [Start(), SetVariable(store.adjusted_bounce_path, None)]
        text "Начать\nигру" font "gui/tahoma.ttf" color "#ffffff" size 30

        imagebutton:
            xpos 50
            idle "settings"
            hover "settings_hover"
            action ShowMenu("preferences")
        text "Настройки" font "gui/tahoma.ttf" color "#ffffff" size 30

        imagebutton:
            xpos 50
            idle "open"
            hover "open_hover"
            action ShowMenu("load")
        text "Открыть\nсохранение" font "gui/tahoma.ttf" color "#ffffff" size 30

        imagebutton:
            xpos 50
            idle "gallery"
            hover "gallery_hover"
            action ShowMenu("gallery")
        text "Мои рисунки" font "gui/tahoma.ttf" color "#ffffff" size 30

        imagebutton:
            xpos 50
            idle "exit"
            hover "exit_hover"
            action Quit()
        text "Выход\nиз системы" font "gui/tahoma.ttf" color "#ffffff" size 30
        textbutton "radio" action Function(toggle_phonk_radio)

    image "gui/xp_menu/browser.png" xsize 1200 ysize 800 xalign 0.5 yalign 0.5

    # Окно браузера
    frame:
        xalign 0.5
        yalign 0.6
        xsize 1150
        ysize 750
        padding (20, 180, 20, 60)
        use social_network_ui


    
init python:
    def get_bounce_path():
        """Возвращает кэшированную траекторию, вычисляя её при первом вызове."""
        if store.adjusted_bounce_path is None:
            store.adjusted_bounce_path = calculate_trajectory((300, 0), (300, 0))
            print(f"🎯 [TRAJECTORY] Вычислено {len(store.adjusted_bounce_path)} точек")
        return store.adjusted_bounce_path

screen screensaver():
    $ path = get_bounce_path()
    # Твое анимированное лого
    add At(
        Transform("sign", xsize=800, ysize=300),
        PathMotion(
            adjusted_bounce_path,
            100.0,
            repeat=False,
            bounce=False,
            sizes=((800, 300))
        )
    )
    # При клике скрываем скринсейвер и обнуляем таймер, чтобы он не сработал мгновенно снова
    button:
        xysize (1.0, 1.0)
        action [Hide("screensaver"), SetVariable("idle_timer", 0)]

init python:
        # ==========================================
    # PHONK RADIO — обёртка с авто-вызовом JS
    # ==========================================
    class PhonkVolume:
        """Обёртка вокруг громкости радио. При изменении значения автоматически
        отправляет новое значение в браузер через Emscripten."""
        
        def __init__(self, initial=0.3):
            self._value = float(initial)
        
        @property
        def value(self):
            return self._value
        
        @value.setter
        def value(self, new_value):
            # Ограничиваем диапазон
            new_value = max(0.0, min(1.0, float(new_value)))
            self._value = new_value
            
            # Отправляем в браузер
            if is_web():
                try:
                    renpy.emscripten.run_script("window.setPhonkVolume(%f);" % new_value)
                    print(f" [RADIO] Громкость обновлена: {new_value:.2f}")
                except Exception as e:
                    print(f"🎵 [RADIO] Ошибка отправки громкости: {e}")
        
        def __float__(self):
            return self._value
        
        def __int__(self):
            return int(self._value)
        
        def __repr__(self):
            return f"{self._value}"

    def play_phonk_radio():
        """Запускает радио-поток."""
        if is_web():
            renpy.emscripten.run_script("window.playPhonkRadio();")

    def stop_phonk_radio():
        """Останавливает радио."""
        if is_web():
            renpy.emscripten.run_script("window.stopPhonkRadio();")

default phonk_volume = PhonkVolume(0.3)