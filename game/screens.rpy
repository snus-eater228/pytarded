################################################################################
## Инициализация
################################################################################

init offset = -1


################################################################################
## Стили
################################################################################

style default:
    properties gui.text_properties()
    language gui.language
style input:
    properties gui.text_properties("input", accent=True)
    adjust_spacing False

style hyperlink_text:
    properties gui.text_properties("hyperlink", accent=True)
    hover_underline True

style gui_text:
    properties gui.text_properties("interface")


style button:
    properties gui.button_properties("button")

style button_text is gui_text:
    properties gui.text_properties("button")
    yalign 0.5


style label_text is gui_text:
    properties gui.text_properties("label", accent=True)

style prompt_text is gui_text:
    properties gui.text_properties("prompt")


style bar:
    ysize gui.bar_size
    left_bar Frame("gui/bar/left.png", gui.bar_borders, tile=gui.bar_tile)
    right_bar Frame("gui/bar/right.png", gui.bar_borders, tile=gui.bar_tile)

style vbar:
    xsize gui.bar_size
    top_bar Frame("gui/bar/top.png", gui.vbar_borders, tile=gui.bar_tile)
    bottom_bar Frame("gui/bar/bottom.png", gui.vbar_borders, tile=gui.bar_tile)

style scrollbar:
    ysize gui.scrollbar_size
    base_bar Frame("gui/scrollbar/horizontal_[prefix_]bar.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame("gui/scrollbar/horizontal_[prefix_]thumb.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)

style vscrollbar:
    xsize gui.scrollbar_size
    base_bar Frame("gui/scrollbar/vertical_[prefix_]bar.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame("gui/scrollbar/vertical_[prefix_]thumb.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)

style slider:
    ysize gui.slider_size
    base_bar Frame("gui/slider/horizontal_[prefix_]bar.png", gui.slider_borders, tile=gui.slider_tile)
    thumb "gui/slider/horizontal_[prefix_]thumb.png"

style vslider:
    xsize gui.slider_size
    base_bar Frame("gui/slider/vertical_[prefix_]bar.png", gui.vslider_borders, tile=gui.slider_tile)
    thumb "gui/slider/vertical_[prefix_]thumb.png"


style frame:
    padding gui.frame_borders.padding
    background Frame("gui/frame.png", gui.frame_borders, tile=gui.frame_tile)

style cap:
    font "gui/tahoma.ttf"
    color "#fff"
    size 36

style t:
    font "gui/tahoma.ttf"
    color "#000"
    size 28

################################################################################
## Внутриигровые экраны
################################################################################

#NOTIFY WIN XP
screen notify_xp(cap, image, t, lab, ext = "jpg"):
    zorder 5
    window at notify_appear:
        ysize 950
        xsize 1000
        background Frame("gui/notify_win.png", 150, 150, 50,50)
        padding (20, 20, 20, 80)
        vbox:
            spacing 20
            text cap ypos -20 xalign 0.5 style "cap"
            text t style "t" xalign 0.1 ypos 0
            add Image(f"images/notify/{image}.{ext}", padding=(50, 50, 50, 50))
            
    timer 0.5 action Jump(lab)

screen block_clicks():
    modal True
    zorder 1000
    button:
        xysize(1.0,1.0)
        action NullAction()





## Экран разговора #############################################################
##
## Экран разговора используется для показа диалога игроку. Он использует два
## параметра — who и what — что, соответственно, имя говорящего персонажа и
## показываемый текст. (Параметр who может быть None, если имя не задано.)
##
## Этот экран должен создать текст с id "what", чтобы Ren'Py могла показать
## текст. Здесь также можно создать наложения с id "who" и id "window", чтобы
## применить к ним настройки стиля.
##
## https://www.renpy.org/doc/html/screen_special.html#say

init python:
    def say_window_transform(trans, st, at):
        global say_window_show_transform

        if not "say_window_show_transform" in globals():
            say_window_show_transform = False

        if not say_window_show_transform:
            trans.yoffset = 250
            say_window_show_transform = True

        progress = st / 0.5  # Нормализуем от 0 до 1
        if progress >= 1.0:
            trans.yoffset = 0
            return None
        else:
            trans.yoffset = 250 * (1 - progress)
            return 0

    def say_window_transform_reset(trans, st, at):
        global say_window_show_transform
        say_window_show_transform = False
        trans.yoffset = 250


transform say_window_animation:
    on show:
        function say_window_transform
    on hide:
        linear 0.3 yoffset 250
        function say_window_transform_reset

transform text_fade_in:
    alpha 0
    linear 0.5 alpha 1

screen say(who, what):
    style_prefix "say"
    zorder 100
    window:
        at say_window_animation
        id "window"
        style "window"
        if who is not None:

            window:
                id "namebox"
                style "namebox"
                text who id "who"

        if what is not None:
            text what id "what"


    ## Если есть боковое изображение ("голова"), показывает её поверх текста.
    ## По стандарту не показывается на варианте для мобильных устройств — мало
    ## места.
    if not renpy.variant("small"):
        add SideImage() xalign 0.0 yalign 1.0


## Делает namebox доступным для стилизации через объект Character.
init python:
    config.character_id_prefixes.append('namebox')
    

style window is default
style say_label is default
style say_dialogue is default
style say_thought is say_dialogue

style namebox is default
style namebox_label is say_label


style window:
    xalign 0.5
    xfill True
    yalign gui.textbox_yalign
    ysize gui.textbox_height

    

style namebox:
    xpos gui.name_xpos
    xanchor gui.name_xalign
    xsize gui.namebox_width
    ypos gui.name_ypos
    ysize gui.namebox_height

    background Frame("gui/namebox.png", gui.namebox_borders, tile=gui.namebox_tile, xalign=gui.name_xalign)
    padding gui.namebox_borders.padding

style say_label:
    properties gui.text_properties("name", accent=True)
    xalign gui.name_xalign
    yalign 0.5

style say_dialogue:
    properties gui.text_properties("dialogue")

    xpos gui.dialogue_xpos
    xsize gui.dialogue_width
    ypos gui.dialogue_ypos
    adjust_spacing False

## Экран ввода #################################################################
##
## Этот экран используется, чтобы показывать renpy.input. Это параметр запроса,
## используемый для того, чтобы дать игроку ввести в него текст.
##
## Этот экран должен создать наложение ввода с id "input", чтобы принять
## различные вводимые параметры.
##
## https://www.renpy.org/doc/html/screen_special.html#input

screen input(prompt):
    style_prefix "input"

    window:

        vbox:
            xanchor gui.dialogue_text_xalign
            xpos gui.dialogue_xpos
            xsize gui.dialogue_width
            ypos gui.dialogue_ypos

            text prompt style "input_prompt"
            input id "input"

style input_prompt is default

style input_prompt:
    xalign gui.dialogue_text_xalign
    properties gui.text_properties("input_prompt")

style input:
    xalign gui.dialogue_text_xalign
    xmaximum gui.dialogue_width


## Экран выбора ################################################################
##
## Этот экран используется, чтобы показывать внутриигровые выборы,
## представленные оператором menu. Один параметр, вложения, список объектов,
## каждый с заголовком и полями действия.
##
## https://www.renpy.org/doc/html/screen_special.html#choice

screen choice(items):
    style_prefix "choice"
    vbox:
        xalign 0.95
        yalign 0.15
        for i in items:
            button:
                text i.caption xalign 0.0
                left_padding 200
                right_padding 180
                top_padding 100
                bottom_padding 100
                action i.action 
                idle_background Frame("gui/textboxes/choice.png", 120, 40, 120, 40)
                hover_background Frame("gui/textboxes/choice_hover.png", 120, 40, 120, 40)


style choice_vbox is vbox
style choice_button is button
style choice_button_text is button_text

style choice_vbox:
    xalign 0.5
    ypos 405
    yanchor 0.25

    spacing gui.choice_spacing

style choice_button is default:
    properties gui.button_properties("choice_button")

style choice_button_text is default:
    properties gui.text_properties("choice_button")


## Экран быстрого меню #########################################################
##
## Быстрое меню показывается внутри игры, чтобы обеспечить лёгкий доступ к
## внеигровым меню.

init python:

    def get_pos(selected):
        return 0 if selected else -400 

    def get_snus(is_opened, is_hovered):
        if not is_hovered:
            return im.Scale("gui/snus/bg.png", 525, 525)
        else:
            return im.Scale("gui/snus/bg_hover.png", 525, 525) if not is_opened else im.Scale("gui/snus/inside.png", 525, 525)
    

transform slide_in_out(selected):
    easein 0.5 ypos get_pos(selected) # Выезжает при selected=True

transform pulse_effect():
    alpha 0.0
    pause 0.2
    alpha 1.0
    pause 0.2
    repeat

transform change_alpha:
    alpha 0.0
    pause 1.0
    block:
        alpha 0.0
        pause 0.2
        alpha 1.0
        pause 0.2
        repeat

transform lilpause:
    alpha 0.0
    pause 1
    alpha 1.0

screen snus_ad():
    add "gui/snus/ad_1.png" at lilpause zoom 0.75
    add "gui/snus/ad_2.png" at change_alpha zoom 0.75

transform rot2(angle):
    rotate angle

image pack:
    "gui/snus/pack.png"
    zoom 0.75
    matrixcolor BrightnessMatrix(0.15)


image color_snus2:
    "gui/snus/pack.png"
    zoom 0.75
    matrixcolor BrightnessMatrix(0.35)
    matrixcolor HueMatrix(-320)
    matrixcolor SaturationMatrix(5)
image color_snus3:
    "gui/snus/pack.png"
    zoom 0.75
    matrixcolor BrightnessMatrix(0.15)
    matrixcolor HueMatrix(760)
image color_snus4:
    "gui/snus/pack.png"
    zoom 0.75
    matrixcolor BrightnessMatrix(0.15)
    matrixcolor HueMatrix(60)
image color_snus5:
    "gui/snus/pack.png"
    zoom 0.75
    matrixcolor BrightnessMatrix(0.15)
    matrixcolor HueMatrix(-160)
image color_snus6:
    "gui/snus/pack.png"
    zoom 0.75
    matrixcolor BrightnessMatrix(0.15)
    matrixcolor HueMatrix(-310)
image color_snus7:
    "gui/snus/pack.png"
    zoom 0.75
    matrixcolor BrightnessMatrix(0.15)
    matrixcolor HueMatrix(460)
image color_snus8:
    "gui/snus/pack.png"
    zoom 0.75
    matrixcolor BrightnessMatrix(0.15)
    matrixcolor HueMatrix(360)

image pack_hover:
    "gui/snus/pack.png"
    zoom 0.75
    matrixcolor HueMatrix(160)
    matrixcolor SaturationMatrix(2)
    matrixcolor BrightnessMatrix(0.35)

image pack_insensitive:
    "gui/snus/pack.png"
    zoom 0.75
    matrixcolor HueMatrix(290)
    matrixcolor SaturationMatrix(-2)
    matrixcolor BrightnessMatrix(-0.15)


#общая для всех снюсов
default is_hovered = False
default is_opened = False
default is_selected = False

screen snus_pack():
    default back_rot = -30
    default skip_rot = 20
    default auto_rot = -80
    default hist_rot = -50
    default conf_rot = 20
    default save_rot = -55
    default ql_rot = 10
    default qs_rot = -20
    # Внутренняя часть снюса (появляется при двойном клике)
    imagebutton:
        idle "color_snus8"
        hover "pack_hover"
        insensitive "pack_insensitive"
        pos (5, 5)
        at rot2(back_rot)
        hovered [SetVariable("is_opened", True), SetVariable("is_hovered", True)]
        action Rollback()
    
    text "откумариться\n(назад)":
        font "gui/Veles.ttf"
        color "#000"
        size 18
        pos (55,55)
        at rot2(back_rot)

    imagebutton:
        idle "color_snus7"
        hover "pack_hover"
        insensitive "pack_insensitive"
        pos (195, 5)
        at rot2(skip_rot)
        hovered [SetVariable("is_opened", True), SetVariable("is_hovered", True)]
        action Skip() alternate Skip(fast=True, confirm=True)
    
    text "раскумариться\n(пропустить)":
        font "gui/Veles.ttf"
        size 18
        pos (240,55)
        at rot2(skip_rot)
        color "#000"

    imagebutton:
        idle "color_snus6"
        hover "pack_hover"
        insensitive "pack_insensitive"
        pos (-15, 185)
        at rot2(auto_rot)
        hovered [SetVariable("is_opened", True), SetVariable("is_hovered", True)]
        action Function(show_bug_report_modal)
    
    text "паль\n(,баг-репорт)":
        font "gui/Veles.ttf"
        size 18
        pos (30,250)
        at rot2(auto_rot)
        color "#000"

    imagebutton:
        idle "color_snus5"
        hover "pack_hover"
        insensitive "pack_insensitive"
        pos (295, 185)
        at rot2(hist_rot)
        hovered [SetVariable("is_opened", True), SetVariable("is_hovered", True)]
        action Function(lambda: renpy.emscripten.run_script("document.getElementById('qr-modal').classList.add('active')"))
    
    text "чужая шайба\n(загрузиться)":
        font "gui/Veles.ttf"
        size 18
        pos (365,245)
        at rot2(hist_rot)
        color "#000"
    
    imagebutton:
        idle "color_snus4"
        hover "pack_hover" 
        insensitive "pack_insensitive"
        pos (185, 85)
        at rot2(conf_rot)
        hovered [SetVariable("is_opened", True), SetVariable("is_hovered", True)]
        action ShowMenu('preferences')
    
    text "сорта снюса\n(конфигурация)":
        font "gui/Veles.ttf"
        size 18
        pos (245,125)
        at rot2(conf_rot)
        color "#000"
    
    imagebutton:
        idle "color_snus3"
        hover "pack_hover"
        insensitive "pack_insensitive"
        pos (45, 55)
        at rot2(save_rot)
        hovered [SetVariable("is_opened", True), SetVariable("is_hovered", True)]
        action ShowMenu("save")
    
    text "прикоп 5 см\n(сохранить)":
        font "gui/Veles.ttf"
        size 18
        pos (105,115)
        at rot2(save_rot)
        color "#000"

    imagebutton:
        idle "color_snus2"
        hover "pack_hover"
        insensitive "pack_insensitive"
        pos (65, 260)
        at rot2(qs_rot)
        hovered [SetVariable("is_opened", True), SetVariable("is_hovered", True)]
        action MainMenu()
    
    text "выплюнуть\n(в меню)":
        font "gui/Veles.ttf"
        size 18
        pos (125,335)
        at rot2(qs_rot)
        color "#000"

    imagebutton:
        idle "pack"
        hover "pack_hover"
        insensitive "pack_insensitive"
        pos (175, 175)
        at rot2(ql_rot)
        hovered [SetVariable("is_opened", True), SetVariable("is_hovered", True)]
        action Function(show_qr_modal)
    
    text "закладка\n(создать\nqr-код)":
        font "gui/Veles.ttf"
        size 18
        pos (245,250)
        at rot2(ql_rot)
        color "#000"

screen quick_menu():
    if not rhythm_game or not rhythm_game.is_playing:
        zorder 100
        
        # Основная кнопка снюса
        imagebutton:
            ypos -400
            idle get_snus(is_opened, is_hovered)
            hover get_snus(is_opened, is_hovered)
            at slide_in_out(is_hovered)
            
            hovered [
                SetVariable("is_hovered", True),
                If(not is_selected, NullAction())
            ]
            unhovered [SetVariable("is_hovered", False), SetVariable("is_opened", False)]
            
            action [
                If(not is_selected, 
                    SetVariable("is_selected", True),
                    [SetVariable("is_opened", True), NullAction()]
                )
            ]
        
        # Показываем рекламу при наведении (если не открыто)
        if is_hovered and not is_opened:
            use snus_ad()
            
        # Показываем содержимое при открытии
        if is_opened:
            use snus_pack()
        
## Данный код гарантирует, что экран быстрого меню будет показан в игре в любое
## время, если только игрок не скроет интерфейс.
init python:
    config.overlay_screens.append("quick_menu")

default quick_menu = False

style quick_button is default
style quick_button_text is button_text

style quick_button:
    properties gui.button_properties("quick_button")

style quick_button_text:
    properties gui.text_properties("quick_button")


################################################################################
## Экраны Главного и Игрового меню
################################################################################

## Экран навигации #############################################################
##
## Этот экран включает в себя главное и игровое меню, и обеспечивает навигацию к
## другим меню и к началу игры.

screen navigation():

    vbox:
        style_prefix "navigation"

        xpos gui.navigation_xpos
        yalign 0.5

        spacing gui.navigation_spacing

        if main_menu:

            textbutton _("Начать") action Start()

        else:

            textbutton _("История") action ShowMenu("history")

            textbutton _("Сохранить") action ShowMenu("save")

        textbutton _("Загрузить") action ShowMenu("load")

        textbutton _("Настройки") action ShowMenu("preferences")

        if _in_replay:

            textbutton _("Завершить повтор") action EndReplay(confirm=True)

        elif not main_menu:

            textbutton _("Главное меню") action MainMenu()

        textbutton _("Об игре") action ShowMenu("about")

        if renpy.variant("pc") or (renpy.variant("web") and not renpy.variant("mobile")):

            ## Помощь не необходима и не относится к мобильным устройствам.
            textbutton _("Помощь") action ShowMenu("help")

        if renpy.variant("pc"):

            ## Кнопка выхода блокирована в iOS и не нужна на Android и в веб-
            ## версии.
            textbutton _("Выход") action Quit(confirm=not main_menu)


style navigation_button is gui_button
style navigation_button_text is gui_button_text

style navigation_button:
    size_group "navigation"
    properties gui.button_properties("navigation_button")

style navigation_button_text:
    properties gui.text_properties("navigation_button")


## Экран главного меню #########################################################
##
## Используется, чтобы показать главное меню после запуска игры.
##
## https://www.renpy.org/doc/html/screen_special.html#main-menu

screen main_menu():
    #tag menu
    style_prefix "main_menu"
    use xp_main_menu()


style main_menu_frame is empty
style main_menu_vbox is vbox
style main_menu_text is gui_text
style main_menu_title is main_menu_text
style main_menu_version is main_menu_text

style main_menu_font:
    properties gui.text_properties("menu")
# style main_menu_frame:
#     xsize 420
#     yfill True

#     background "gui/overlay/main_menu.png"

# style main_menu_vbox:
#     xalign 1.0
#     xoffset -30
#     xmaximum 1200
#     yalign 1.0
#     yoffset -30

style main_menu_text:
    properties gui.text_properties("main_menu", accent=True)

style main_menu_title:
    properties gui.text_properties("title")

style main_menu_version:
    properties gui.text_properties("version")




## Экран игрового меню #########################################################
##
## Всё это показывает основную, обобщённую структуру экрана игрового меню. Он
## вызывается с экраном заголовка и показывает фон, заголовок и навигацию.
##
## Параметр scroll может быть None или один из "viewport" или "vpgrid". Этот
## экран предназначен для использования с одним или несколькими дочерними
## элементами, которые трансклюдируются (помещаются) внутрь него.

screen game_menu(title, scroll=None, yinitial=0.0, spacing=0):

    style_prefix "game_menu"

    if main_menu:
        add gui.main_menu_background
    else:
        add gui.game_menu_background

    frame:
        style "game_menu_outer_frame"

        hbox:

            ## Резервирует пространство для навигации.
            frame:
                style "game_menu_navigation_frame"

            frame:
                style "game_menu_content_frame"

                if scroll == "viewport":

                    viewport:
                        yinitial yinitial
                        scrollbars "vertical"
                        mousewheel True
                        draggable True
                        pagekeys True

                        side_yfill True

                        vbox:
                            spacing spacing

                            transclude

                elif scroll == "vpgrid":

                    vpgrid:
                        cols 1
                        yinitial yinitial

                        scrollbars "vertical"
                        mousewheel True
                        draggable True
                        pagekeys True

                        side_yfill True

                        spacing spacing

                        transclude

                else:

                    transclude

    use navigation

    textbutton _("Вернуться"):
        style "return_button"

        action Return()

    label title

    if main_menu:
        key "game_menu" action ShowMenu("main_menu")


style game_menu_outer_frame is empty
style game_menu_navigation_frame is empty
style game_menu_content_frame is empty
style game_menu_viewport is gui_viewport
style game_menu_side is gui_side
style game_menu_scrollbar is gui_vscrollbar

style game_menu_label is gui_label
style game_menu_label_text is gui_label_text

style return_button is navigation_button
style return_button_text is navigation_button_text

style game_menu_outer_frame:
    bottom_padding 45
    top_padding 180

    background "gui/overlay/game_menu.png"

style game_menu_navigation_frame:
    xsize 420
    yfill True

style game_menu_content_frame:
    left_margin 60
    right_margin 30
    top_margin 15

style game_menu_viewport:
    xsize 1380

style game_menu_vscrollbar:
    unscrollable gui.unscrollable

style game_menu_side:
    spacing 15

style game_menu_label:
    xpos 75
    ysize 180

style game_menu_label_text:
    size gui.title_text_size
    color gui.accent_color
    yalign 0.5

style return_button:
    xpos gui.navigation_xpos
    yalign 1.0
    yoffset -45


## Экран Об игре ###############################################################
##
## Этот экран показывает авторскую информацию об игре и Ren'Py.
##
## В этом экране нет ничего особенного, и он служит только примером того, каким
## можно сделать свой экран.

screen about():

    tag menu

    ## Этот оператор включает игровое меню внутрь этого экрана. Дочерний vbox
    ## включён в порт просмотра внутри экрана игрового меню.
    use game_menu(_("Об игре"), scroll="viewport"):

        style_prefix "about"

        vbox:

            label "[config.name!t]"
            text _("Версия [config.version!t]\n")

            ## gui.about обычно установлено в options.rpy.
            if gui.about:
                text "[gui.about!t]\n"

            text _("Сделано с помощью {a=https://www.renpy.org/}Ren'Py{/a} [renpy.version_only].\n\n[renpy.license!t]")


style about_label is gui_label
style about_label_text is gui_label_text
style about_text is gui_text

style about_label_text:
    size gui.label_text_size


## Экраны загрузки и сохранения ################################################
##
## Эти экраны ответственны за возможность сохранять и загружать игру. Так
## как они почти одинаковые, оба реализованы по правилам третьего экрана —
## file_slots.
##
## https://www.renpy.org/doc/html/screen_special.html#save 

screen save():

    tag menu

    use file_slots(_("Сохранить"))


screen load():

    tag menu

    use file_slots(_("Загрузить"))


screen file_slots(title):

    default page_name_value = FilePageNameInputValue(pattern=_("{} страница"), auto=_("Автосохранения"), quick=_("Быстрые сохранения"))

    use game_menu(title):

        fixed:

            ## Это гарантирует, что ввод будет принимать enter перед остальными
            ## кнопками.
            order_reverse True

            ## Номер страницы, который может быть изменён посредством клика на
            ## кнопку.
            button:
                style "page_label"

                key_events True
                xalign 0.5
                action page_name_value.Toggle()

                input:
                    style "page_label_text"
                    value page_name_value

            ## Таблица слотов.
            grid gui.file_slot_cols gui.file_slot_rows:
                style_prefix "slot"

                xalign 0.5
                yalign 0.5

                spacing gui.slot_spacing

                for i in range(gui.file_slot_cols * gui.file_slot_rows):

                    $ slot = i + 1

                    button:
                        action FileAction(slot)

                        has vbox

                        add FileScreenshot(slot) xalign 0.5

                        text FileTime(slot, format=_("{#file_time}%A, %d %B %Y, %H:%M"), empty=_("Пустой слот")):
                            style "slot_time_text"

                        text FileSaveName(slot):
                            style "slot_name_text"

                        key "save_delete" action FileDelete(slot)

            ## Кнопки для доступа к другим страницам.
            vbox:
                style_prefix "page"

                xalign 0.5
                yalign 1.0

                hbox:
                    xalign 0.5

                    spacing gui.page_spacing

                    textbutton _("<") action FilePagePrevious()
                    key "save_page_prev" action FilePagePrevious()

                    if config.has_autosave:
                        textbutton _("{#auto_page}А") action FilePage("auto")

                    if config.has_quicksave:
                        textbutton _("{#quick_page}Б") action FilePage("quick")

                    ## range(1, 10) задаёт диапазон значений от 1 до 9.
                    for page in range(1, 10):
                        textbutton "[page]" action FilePage(page)

                    textbutton _(">") action FilePageNext()
                    key "save_page_next" action FilePageNext()

                if config.has_sync:
                    if CurrentScreenName() == "save":
                        textbutton _("Загрузить Sync"):
                            action UploadSync()
                            xalign 0.5
                    else:
                        textbutton _("Скачать Sync"):
                            action DownloadSync()
                            xalign 0.5


style page_label is gui_label
style page_label_text is gui_label_text
style page_button is gui_button
style page_button_text is gui_button_text

style slot_button is gui_button
style slot_button_text is gui_button_text
style slot_time_text is slot_button_text
style slot_name_text is slot_button_text

style page_label:
    xpadding 75
    ypadding 5

style page_label_text:
    textalign 0.5
    layout "subtitle"
    hover_color gui.hover_color

style page_button:
    properties gui.button_properties("page_button")

style page_button_text:
    properties gui.text_properties("page_button")

style slot_button:
    properties gui.button_properties("slot_button")

style slot_button_text:
    properties gui.text_properties("slot_button")


## Экран настроек ##############################################################
##
## Экран настроек позволяет игроку настраивать игру под себя.
##
## https://www.renpy.org/doc/html/screen_special.html#preferences

screen preferences():

    tag menu

    use game_menu(_("Настройки"), scroll="viewport"):

        vbox:

            hbox:
                box_wrap True

                if renpy.variant("pc") or renpy.variant("web"):

                    vbox:
                        style_prefix "radio"
                        label _("Режим экрана")
                        textbutton _("Оконный") action Preference("display", "window")
                        textbutton _("Полный") action Preference("display", "fullscreen")

                vbox:
                    style_prefix "check"
                    label _("Пропуск")
                    textbutton _("Всего текста") action Preference("skip", "toggle")
                    textbutton _("После выборов") action Preference("after choices", "toggle")
                    textbutton _("Переходов") action InvertSelected(Preference("transitions", "toggle"))

                ## Дополнительные vbox'ы типа "radio_pref" или "check_pref"
                ## могут быть добавлены сюда для добавления новых настроек.

            null height (4 * gui.pref_spacing)

            hbox:
                style_prefix "slider"
                box_wrap True

                vbox:

                    label _("Скорость текста")

                    bar value Preference("text speed")

                    label _("Скорость авточтения")

                    bar value Preference("auto-forward time")

                vbox:

                    if config.has_music:
                        label _("Громкость музыки")

                        hbox:
                            bar value Preference("music volume")

                    if config.has_sound:

                        label _("Громкость звуков")

                        hbox:
                            bar value Preference("sound volume")

                            if config.sample_sound:
                                textbutton _("Тест") action Play("sound", config.sample_sound)


                    if config.has_voice:
                        label _("Громкость голоса")

                        hbox:
                            bar value Preference("voice volume")

                            if config.sample_voice:
                                textbutton _("Тест") action Play("voice", config.sample_voice)

                    if config.has_music or config.has_sound or config.has_voice:
                        null height gui.pref_spacing

                        textbutton _("Без звука"):
                            action Preference("all mute", "toggle")
                            style "mute_all_button"


style pref_label is gui_label
style pref_label_text is gui_label_text
style pref_vbox is vbox

style radio_label is pref_label
style radio_label_text is pref_label_text
style radio_button is gui_button
style radio_button_text is gui_button_text
style radio_vbox is pref_vbox

style check_label is pref_label
style check_label_text is pref_label_text
style check_button is gui_button
style check_button_text is gui_button_text
style check_vbox is pref_vbox

style slider_label is pref_label
style slider_label_text is pref_label_text
style slider_slider is gui_slider
style slider_button is gui_button
style slider_button_text is gui_button_text
style slider_pref_vbox is pref_vbox

style mute_all_button is check_button
style mute_all_button_text is check_button_text

style pref_label:
    top_margin gui.pref_spacing
    bottom_margin 3

style pref_label_text:
    yalign 1.0

style pref_vbox:
    xsize 338

style radio_vbox:
    spacing gui.pref_button_spacing

style radio_button:
    properties gui.button_properties("radio_button")
    foreground "gui/button/radio_[prefix_]foreground.png"

style radio_button_text:
    properties gui.text_properties("radio_button")

style check_vbox:
    spacing gui.pref_button_spacing

style check_button:
    properties gui.button_properties("check_button")
    foreground "gui/button/check_[prefix_]foreground.png"

style check_button_text:
    properties gui.text_properties("check_button")

style slider_slider:
    xsize 525

style slider_button:
    properties gui.button_properties("slider_button")
    yalign 0.5
    left_margin 15

style slider_button_text:
    properties gui.text_properties("slider_button")

style slider_vbox:
    xsize 675


## Экран истории ###############################################################
##
## Этот экран показывает игроку историю диалогов. Хотя в этом экране нет ничего
## особенного, он имеет доступ к истории диалогов, хранимом в _history_list.
##
## https://www.renpy.org/doc/html/history.html

screen history():

    tag menu

    ## Избегайте предсказывания этого экрана, так как он может быть очень
    ## массивным.
    predict False

    use game_menu(_("История"), scroll=("vpgrid" if gui.history_height else "viewport"), yinitial=1.0, spacing=gui.history_spacing):

        style_prefix "history"

        for h in _history_list:

            window:

                ## Это всё правильно уравняет, если history_height будет
                ## установлен на None.
                has fixed:
                    yfit True

                if h.who:

                    label h.who:
                        style "history_name"
                        substitute False

                        ## Берёт цвет из who параметра персонажа, если он
                        ## установлен.
                        if "color" in h.who_args:
                            text_color h.who_args["color"]

                $ what = renpy.filter_text_tags(h.what, allow=gui.history_allow_tags)
                text what:
                    substitute False

        if not _history_list:
            label _("История диалогов пуста.")


## Это определяет, какие теги могут отображаться на экране истории.

define gui.history_allow_tags = { "alt", "noalt", "rt", "rb", "art" }


style history_window is empty

style history_name is gui_label
style history_name_text is gui_label_text
style history_text is gui_text

style history_label is gui_label
style history_label_text is gui_label_text

style history_window:
    xfill True
    ysize gui.history_height

style history_name:
    xpos gui.history_name_xpos
    xanchor gui.history_name_xalign
    ypos gui.history_name_ypos
    xsize gui.history_name_width

style history_name_text:
    min_width gui.history_name_width
    textalign gui.history_name_xalign

style history_text:
    xpos gui.history_text_xpos
    ypos gui.history_text_ypos
    xanchor gui.history_text_xalign
    xsize gui.history_text_width
    min_width gui.history_text_width
    textalign gui.history_text_xalign
    layout ("subtitle" if gui.history_text_xalign else "tex")

style history_label:
    xfill True

style history_label_text:
    xalign 0.5


## Экран помощи ################################################################
##
## Экран, дающий информацию о клавишах управления. Он использует другие экраны
## (keyboard_help, mouse_help, и gamepad_help), чтобы показывать актуальную
## помощь.

screen help():

    tag menu

    default device = "keyboard"

    use game_menu(_("Помощь"), scroll="viewport"):

        style_prefix "help"

        vbox:
            spacing 23

            hbox:

                textbutton _("Клавиатура") action SetScreenVariable("device", "keyboard")
                textbutton _("Мышь") action SetScreenVariable("device", "mouse")

                if GamepadExists():
                    textbutton _("Геймпад") action SetScreenVariable("device", "gamepad")

            if device == "keyboard":
                use keyboard_help
            elif device == "mouse":
                use mouse_help
            elif device == "gamepad":
                use gamepad_help


screen keyboard_help():

    hbox:
        label _("Enter")
        text _("Прохождение диалогов, активация интерфейса.")

    hbox:
        label _("Пробел")
        text _("Прохождение диалогов без возможности делать выбор.")

    hbox:
        label _("Стрелки")
        text _("Навигация по интерфейсу.")

    hbox:
        label _("Esc")
        text _("Вход в игровое меню.")

    hbox:
        label _("Ctrl")
        text _("Пропускает диалоги, пока зажат.")

    hbox:
        label _("Tab")
        text _("Включает режим пропуска.")

    hbox:
        label _("Page Up")
        text _("Откат назад по сюжету игры.")

    hbox:
        label _("Page Down")
        text _("Откатывает предыдущее действие вперёд.")

    hbox:
        label "H"
        text _("Скрывает интерфейс пользователя.")

    hbox:
        label "S"
        text _("Делает снимок экрана.")

    hbox:
        label "V"
        text _("Включает поддерживаемый {a=https://www.renpy.org/l/voicing}синтезатор речи{/a}.")

    hbox:
        label "Shift+A"
        text _("Открывает меню специальных возможностей.")


screen mouse_help():

    hbox:
        label _("Левый клик")
        text _("Прохождение диалогов, активация интерфейса.")

    hbox:
        label _("Клик колёсиком")
        text _("Скрывает интерфейс пользователя.")

    hbox:
        label _("Правый клик")
        text _("Вход в игровое меню.")

    hbox:
        label _("Колёсико вверх")
        text _("Откат назад по сюжету игры.")

    hbox:
        label _("Колёсико вниз")
        text _("Откатывает предыдущее действие вперёд.")


screen gamepad_help():

    hbox:
        label _("Правый триггер\nA/Нижняя кнопка")
        text _("Прохождение диалогов, активация интерфейса.")

    hbox:
        label _("Левый Триггер\nЛевый Бампер")
        text _("Откат назад по сюжету игры.")

    hbox:
        label _("Правый бампер")
        text _("Откатывает предыдущее действие вперёд.")

    hbox:
        label _("Крестовина, Стики")
        text _("Навигация по интерфейсу.")

    hbox:
        label _("Старт, Гид, B/Правая кнопка")
        text _("Вход в игровое меню.")

    hbox:
        label _("Y/Верхняя кнопка")
        text _("Скрывает интерфейс пользователя.")

    textbutton _("Калибровка") action GamepadCalibrate()


style help_button is gui_button
style help_button_text is gui_button_text
style help_label is gui_label
style help_label_text is gui_label_text
style help_text is gui_text

style help_button:
    properties gui.button_properties("help_button")
    xmargin 12

style help_button_text:
    properties gui.text_properties("help_button")

style help_label:
    xsize 375
    right_padding 30

style help_label_text:
    size gui.text_size
    xalign 1.0
    textalign 1.0



################################################################################
## Дополнительные экраны
################################################################################


## Экран подтверждения #########################################################
##
## Экран подтверждения вызывается, когда Ren'Py хочет спросить у игрока вопрос
## Да или Нет.
##
## https://www.renpy.org/doc/html/screen_special.html#confirm

screen confirm(message, yes_action, no_action):

    ## Гарантирует, что другие экраны будут недоступны, пока показан этот экран.
    modal True
    if rhythm_game:
        $ rhythm_game.stop()
    zorder 200

    style_prefix "confirm"

    add "gui/overlay/confirm.png"

    frame:

        vbox:
            xalign .5
            yalign .5
            spacing 45

            label _(message):
                style "confirm_prompt"
                xalign 0.5

            hbox:
                xalign 0.5
                spacing 150

                textbutton _("Бурмалда") action yes_action
                textbutton _("Не бурмалда") action no_action

    ## Правый клик и esc, как ответ "Нет".
    key "game_menu" action no_action


style confirm_frame is gui_frame
style confirm_prompt is gui_prompt
style confirm_prompt_text is gui_prompt_text
style confirm_button is gui_medium_button
style confirm_button_text is gui_medium_button_text

style confirm_frame:
    background Frame([ "gui/confirm_frame.png", "gui/frame.png"], gui.confirm_frame_borders, tile=gui.frame_tile)
    padding gui.confirm_frame_borders.padding
    xalign .5
    yalign .5

style confirm_prompt_text:
    textalign 0.5
    layout "subtitle"

style confirm_button:
    properties gui.button_properties("confirm_button")

style confirm_button_text:
    properties gui.text_properties("confirm_button")


## Экран индикатора пропуска ###################################################
##
## Экран индикатора пропуска появляется для того, чтобы показать, что идёт
## пропуск.
##
## https://www.renpy.org/doc/html/screen_special.html#skip-indicator

screen skip_indicator():

    zorder 100
    style_prefix "skip"

    frame:

        hbox:
            spacing 9

            text _("Пропускаю")

            text "▸" at delayed_blink(0.0, 1.0) style "skip_triangle"
            text "▸" at delayed_blink(0.2, 1.0) style "skip_triangle"
            text "▸" at delayed_blink(0.4, 1.0) style "skip_triangle"


## Эта трансформация используется, чтобы мигать стрелками одна за другой.
transform delayed_blink(delay, cycle):
    alpha .5

    pause delay

    block:
        linear .2 alpha 1.0
        pause .2
        linear .2 alpha 0.5
        pause (cycle - .4)
        repeat


style skip_frame is empty
style skip_text is gui_text
style skip_triangle is skip_text

style skip_frame:
    ypos gui.skip_ypos
    background Frame("gui/skip.png", gui.skip_frame_borders, tile=gui.frame_tile)
    padding gui.skip_frame_borders.padding

style skip_text:
    size gui.notify_text_size

style skip_triangle:
    ## Нам надо использовать шрифт, имеющий в себе символ U+25B8 (стрелку выше).
    font "DejaVuSans.ttf"


## Экран уведомлений ###########################################################
##
## Экран уведомлений используется, чтобы показать игроку оповещение. (Например,
## когда игра автосохранилась, или был сделан скриншот)
##
## https://www.renpy.org/doc/html/screen_special.html#notify-screen

screen notify(message):

    zorder 100
    style_prefix "notify"

    window at notify_appear:
        text "[message!tq]" ypos 80 xpos 80

    timer 3.25 action Hide('notify')


transform notify_appear:
    on show:
        alpha 0
        linear .25 alpha 1.0
    on hide:
        linear .5 alpha 0.0


style notify_text is gui_text

style notify_window:
    xalign gui.notify_xalign
    yalign 0
    xsize 512
    ysize 320
    background im.Scale("gui/textboxes/notify.png", 512, 320)
    padding gui.notify_frame_borders.padding

style notify_text:
    properties gui.text_properties("notify")

init python:
    def stat_text(stat):
        if stat == "brain_dave":
            return "плюсик к сознательности твоего друга. ему полезно"
        if stat == "brain_lars":
            return "плюсик к собственной сознательности. типа умный"
        if stat == "will":
            return "плюсик к силе воли. сможешь быковать на кого хочешь"
        if stat == "respect":
            return "плюсик к уважению. teacher's pet такой типичный"

screen stat(s):
    window at notify_appear:
        style "default"
        xpos 1200
        yalign 0.2
        add im.Scale("gui/textboxes/notify.png", 580, 340)
        hbox:
            add im.Scale("gui/"+s+".png", 125,125) xpos 75 ypos 75
            text stat_text(s) xsize 300 xpos 75 ypos 75
    timer 3.25 action Hide('stat')

transform alpha_dissolve:
    alpha 0.0
    linear 0.5 alpha 1.0
    on hide:
        linear 0.5 alpha 0

screen timez:
    timer 0.05 repeat True action If(time > 0, true=SetVariable('time', time - 0.05), false=[Hide('timez'), Jump(timer_jump)])
    bar:
        value AnimatedValue (value=4.0, range=time*10.0,)
        xpos 250 yalign 0.1 xmaximum 300 at alpha_dissolve
    add "clock"
    


## Экран NVL ###################################################################
##
## Этот экран используется в диалогах и меню режима NVL.
##
## https://www.renpy.org/doc/html/screen_special.html#nvl

init python:

    def nontransient_nvl(mode, old_modes):

        if mode == 'say' or mode == 'menu':
            widget_properties, dialogue, show_args = _m1_00nvl_mode__nvl_screen_dialogue()
            if dialogue:
                renpy.show_screen('nvl', _layer=config.nvl_layer, _widget_properties=widget_properties, dialogue=dialogue, **show_args)

        elif mode == 'nvl':
            nvl_hide(None)

    config.mode_callbacks.append(nontransient_nvl)

screen nvl(dialogue, items=[]):
    window:
        if nvl_mode == "board":
            xalign 0.9
            style "nvl_window"
        if nvl_mode == "computer":
            xalign 1.0
            yalign 1.0
            style "nvl_computer_window"
        if nvl_mode == "print":
            xalign 1.0
            yalign 1.0
            style "nvl_print"

        has vbox:
            spacing gui.nvl_spacing

            ## Показывает диалог или в vpgrid, или в vbox.
        if gui.nvl_height:

            vpgrid:
                cols 1
                yinitial 1.0

                use nvl_dialogue(dialogue)

        else:

            use nvl_dialogue(dialogue)

            ## Показывает меню, если есть. Меню может показываться некорректно, если
            ## config.narrator_menu установлено на True.
        for i in items:

            textbutton i.caption:
                action i.action
                style "nvl_button"

    add SideImage() xalign 0.0 yalign 1.0


screen nvl_dialogue(dialogue):
    for d in dialogue:

        window:
            id d.window_id

            fixed:
                yfit gui.nvl_height is None

                if d.who is not None:

                    text d.who:
                        id d.who_id

                text d.what:
                    if nvl_mode == "print":
                        size 14
                
                    id d.what_id


## Это контролирует максимальное число строк NVL, могущих показываться за раз.
define config.nvl_list_length = gui.nvl_list_length

style nvl_window is default
style nvl_entry is default

style nvl_label is say_label
style nvl_dialogue is say_dialogue


style nvl_button is button
style nvl_button_text is button_text

style nvl_window:
    xsize 600
    ysize None

    background Frame("gui/nvl.png", 10,10,10,10)
    padding gui.nvl_borders.padding

style nvl_computer_window:
    xsize 800
    ysize 600

    background Frame("gui/nvl_computer.jpg", 20,20,20,20)
    padding (120, 120, 10, 10)

style nvl_print:
    xsize 600
    ysize 400

    background Frame("gui/nvl3.jpg", 20,20,20,20)
    padding (-30, 40, 10, 10)

style nvl_entry:
    xfill True
    ysize gui.nvl_height

style nvl_label:
    xpos gui.nvl_name_xpos
    xanchor gui.nvl_name_xalign
    ypos gui.nvl_name_ypos
    yanchor 0.0
    xsize gui.nvl_name_width
    min_width gui.nvl_name_width
    textalign gui.nvl_name_xalign

style nvl_dialogue:
    xpos gui.nvl_text_xpos
    xanchor gui.nvl_text_xalign
    ypos gui.nvl_text_ypos
    xsize gui.nvl_text_width
    min_width gui.nvl_text_width
    textalign gui.nvl_text_xalign
    layout ("subtitle" if gui.nvl_text_xalign else "tex")

style nvl_thought:
    xpos gui.nvl_thought_xpos
    xanchor gui.nvl_thought_xalign
    ypos gui.nvl_thought_ypos
    xsize gui.nvl_thought_width
    min_width gui.nvl_thought_width
    textalign gui.nvl_thought_xalign
    layout ("subtitle" if gui.nvl_text_xalign else "tex")

style nvl_button:
    properties gui.button_properties("nvl_button")
    xpos gui.nvl_button_xpos
    xanchor gui.nvl_button_xalign

style nvl_button_text:
    properties gui.text_properties("nvl_button")


## Пузырьковый экран ###########################################################
##
## Экран пузырьков используется для отображения диалога игроку при использовании
## речевых пузырьков. Экран пузырьков принимает те же параметры, что и экран
## say, должен создать отображаемый объект с id "what", и может создавать
## отображаемые объекты с id "namebox", "who" и "window".
##
## https://www.renpy.org/doc/html/bubble.html#bubble-screen

screen bubble(who, what):
    style_prefix "bubble"

    window:
        id "window"

        if who is not None:

            window:
                id "namebox"
                style "bubble_namebox"

                text who:
                    id "who"

        text what:
            id "what"

style bubble_window is empty
style bubble_namebox is empty
style bubble_who is default
style bubble_what is default

style bubble_window:
    xpadding 30
    top_padding 5
    bottom_padding 5

style bubble_namebox:
    xalign 0.5

style bubble_who:
    xalign 0.5
    textalign 0.5
    color "#000"

style bubble_what:
    align (0.5, 0.5)
    text_align 0.5
    layout "subtitle"
    color "#000"

define bubble.frame = Frame("gui/bubble.png", 55, 55, 55, 95)
define bubble.thoughtframe = Frame("gui/thoughtbubble.png", 55, 55, 55, 55)

define bubble.properties = {
    "bottom_left" : {
        "window_background" : Transform(bubble.frame, xzoom=1, yzoom=1),
        "window_bottom_padding" : 27,
    },

    "bottom_right" : {
        "window_background" : Transform(bubble.frame, xzoom=-1, yzoom=1),
        "window_bottom_padding" : 27,
    },

    "top_left" : {
        "window_background" : Transform(bubble.frame, xzoom=1, yzoom=-1),
        "window_top_padding" : 27,
    },

    "top_right" : {
        "window_background" : Transform(bubble.frame, xzoom=-1, yzoom=-1),
        "window_top_padding" : 27,
    },

    "thought" : {
        "window_background" : bubble.thoughtframe,
    }
}

define bubble.expand_area = {
    "bottom_left" : (0, 0, 0, 22),
    "bottom_right" : (0, 0, 0, 22),
    "top_left" : (0, 22, 0, 0),
    "top_right" : (0, 22, 0, 0),
    "thought" : (0, 0, 0, 0),
}



################################################################################
## Мобильные варианты
################################################################################

style pref_vbox:
    variant "medium"
    xsize 675

## Раз мышь может не использоваться, мы заменили быстрое меню версией,
## использующей меньше кнопок, но больших по размеру, чтобы их было легче
## касаться.
screen quick_menu():
    variant "touch"

    zorder 100

    if quick_menu:

        hbox:
            style_prefix "quick"

            xalign 0.5
            yalign 1.0

            textbutton _("Назад") action Rollback()
            textbutton _("Пропуск") action Skip() alternate Skip(fast=True, confirm=True)
            textbutton _("Авто") action Preference("auto-forward", "toggle")
            textbutton _("Меню") action ShowMenu()


style window:
    variant "small"

style radio_button:
    variant "small"
    foreground "gui/phone/button/radio_[prefix_]foreground.png"

style check_button:
    variant "small"
    foreground "gui/phone/button/check_[prefix_]foreground.png"

style nvl_window:
    variant "small"
    background "gui/phone/nvl.png"

style main_menu_frame:
    variant "small"
    background "gui/phone/overlay/main_menu.png"

style game_menu_outer_frame:
    variant "small"
    background "gui/phone/overlay/game_menu.png"

style game_menu_navigation_frame:
    variant "small"
    xsize 510

style game_menu_content_frame:
    variant "small"
    top_margin 0

style pref_vbox:
    variant "small"
    xsize 600

style bar:
    variant "small"
    ysize gui.bar_size
    left_bar Frame("gui/phone/bar/left.png", gui.bar_borders, tile=gui.bar_tile)
    right_bar Frame("gui/phone/bar/right.png", gui.bar_borders, tile=gui.bar_tile)

style vbar:
    variant "small"
    xsize gui.bar_size
    top_bar Frame("gui/phone/bar/top.png", gui.vbar_borders, tile=gui.bar_tile)
    bottom_bar Frame("gui/phone/bar/bottom.png", gui.vbar_borders, tile=gui.bar_tile)

style scrollbar:
    variant "small"
    ysize gui.scrollbar_size
    base_bar Frame("gui/phone/scrollbar/horizontal_[prefix_]bar.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame("gui/phone/scrollbar/horizontal_[prefix_]thumb.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)

style vscrollbar:
    variant "small"
    xsize gui.scrollbar_size
    base_bar Frame("gui/phone/scrollbar/vertical_[prefix_]bar.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame("gui/phone/scrollbar/vertical_[prefix_]thumb.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)

style slider:
    variant "small"
    ysize gui.slider_size
    base_bar Frame("gui/phone/slider/horizontal_[prefix_]bar.png", gui.slider_borders, tile=gui.slider_tile)
    thumb "gui/phone/slider/horizontal_[prefix_]thumb.png"

style vslider:
    variant "small"
    xsize gui.slider_size
    base_bar Frame("gui/phone/slider/vertical_[prefix_]bar.png", gui.vslider_borders, tile=gui.slider_tile)
    thumb "gui/phone/slider/vertical_[prefix_]thumb.png"

style slider_vbox:
    variant "small"
    xsize None

style slider_slider:
    variant "small"
    xsize 900

###### Экран ноутбук (ниче не делает) ########
screen laptop():
    imagebutton:
        xalign 0.65
        yalign 0.5
        idle im.Scale("images/laptop_unhover.png", 250, 200)
        hover im.Scale("images/laptop_hover.png", 250, 200)
        action NullAction()


#TERMINAL (for cyber notify)
screen cyber_notify(msg):
    zorder 100
    frame at notify_appear:
        xalign 0.9
        yalign 0.05
        xsize 700
        padding (240,74,0,0)
        background Image("gui/ubuntu.png")
        text msg font "gui/tahoma.ttf" size 24 color "#fff"
    timer 7.0 action Hide("cyber_notify")

init python:
    def get_list():
        return [f"{k}.jpg" for k in persistent.gallery.keys()]

    def process_terminal_command(val):
        val = val.strip().lower() 
        if val == "":
            return
        elif val == "ls":
            renpy.store.ls = get_list()
            renpy.show_screen("ls", store.ls)
        elif val.startswith("xdg-open"):
            renpy.hide_screen("notify")
            file = val.split(" ")[1]
            file_path=file.replace(".jpg", "")
            if file_path in persistent.gallery.keys():
                renpy.show_screen("gallery_image", f"images/gallery/{file}")
            else:
                renpy.show_screen("term_notify", f"Файл {file} не найден!")
        elif val == "exit":
            renpy.hide_screen("notify")
            renpy.show_screen(_screen_name="main_menu")  # Use call, not show_screen, for proper navigation
        else:
            renpy.hide_screen("notify")
            renpy.show_screen("term_notify", "Ошибка в команде: " + val + "!\nДоступные команды: ls - вывод содержимого папки, xdg-open example.jpg - откроет картинку, exit - выход из галереи.")
        renpy.store.inpval = ""

    renpy.config.keymap["input_enter"].remove('K_RETURN')
    renpy.config.keymap["input_enter"].remove('K_KP_ENTER')
screen gallery_image(file):
    vbox:
        yalign 0.5
        xalign 0.5
        frame:
                background "#575651"
                xsize 800
                ysize 50
                padding (100,10,100,10)
                
                text "cyber_lars2007@ubuntu: ~" font "gui/UbuntuMono-R.ttf" color "#ffffff" size 24 xalign 0.5
                button:
                    ypos -148
                    text "." font "gui/UbuntuMono-R.ttf"  color "#ff5f56" size 210 
                    action Hide("gallery_image")
                    xpos 620
                text "x" font "gui/UbuntuMono-R.ttf"  color "#fff" size 30 xpos 671
        imagebutton idle im.Scale(file, 800,800) hover im.Scale(file, 800,800) action Hide("gallery_image") xalign 0.5 yalign 0.5
screen gallery():
    default input_value = VariableInputValue("inpval", returnable=True)
    tag menu
    key "K_RETURN" action Function(process_terminal_command, inpval)
    key "K_KP_ENTER" action Function(process_terminal_command, inpval)
    # Background terminal window
    window:
        style "terminal_window"
        xalign 0.5
        yalign 0.5
        has vbox
        vbox:
            # Top bar (fake title bar)
            frame:
                background "#575651"
                xfill True
                ysize 50
                padding (100,10,100,10)
                
                text "cyber_lars2007@ubuntu: ~" font "gui/UbuntuMono-R.ttf" color "#ffffff" size 24 xalign 0.5
                button:
                    ypos -148
                    text "." font "gui/UbuntuMono-R.ttf"  color "#ff5f56" size 210 
                    action ShowMenu("main_menu")
                    xpos 1720
                text "x" font "gui/UbuntuMono-R.ttf"  color "#fff" size 30 xpos 1771

            # Terminal body
            frame:
                background "#300a24"
                xfill True
                yfill True
                padding (10,10,10,10)
                has vbox
                vbox:
                # Terminal prompt
                    hbox:
                        xmaximum 1900
                        text "cyber_lars2007@ubuntu" font  "gui/UbuntuMono-R.ttf"  color "#00ff00" size 26
                        text ":" font  "gui/UbuntuMono-R.ttf"  color "#ffffff" size 26
                        text "/gallery" color "#457db8" font "gui/UbuntuMono-R.ttf"  size 26
                        text "$  " font  "gui/UbuntuMono-R.ttf"  color "#ffffff" size 26
                        input value input_value copypaste True id "command_input" allow ".-abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_ " length 30 font "gui/UbuntuMono-R.ttf" color "#ffffff" size 26
                

style terminal_window is default:
    background "#98333d"
    padding (2, 2, 2, 2)
    xsize None
    ysize None

screen term_notify(_text):
    tag notify
    button:
        text _text font  "gui/UbuntuMono-R.ttf" color "#ffffff" size 26
        ypos 100 
        action Hide("term_notify")
        xpos 5
    
screen ls(items):
    tag notify
    vbox:
        for _text in items:
            button:
                text _text font  "gui/UbuntuMono-R.ttf" color "#ffffff" size 26
                ypos 100 
                action Hide("ls")
                xpos 5
                bottom_margin 5

# ЭКРАН РИКРОЛЛА
screen rickroll():
    zorder 100      # Гарантирует, что экран будет ПОВЕРХ всего (даже поверх браузера)
    modal True      # Блокирует клики по нижним слоям, пока открыто видео
    
    # Полупрозрачное затемнение фона для фокуса на видео (опционально)
    add "#000000cc" xysize (1.0, 1.0)

    # Контейнер для видео и кнопки закрытия
    fixed:
        xalign 0.5
        yalign 0.5
        
        # Проигрывание видео внутри экрана.
        # ВАЖНО: Укажи здесь реальный путь к твоему видеофайлу (например, "gui/xp_menu/rickroll.webm")
        add Movie(play="gui/xp_menu/rickroll.webm", loop=True, xsize=642, ysize=361) xalign 0.58 yalign 0.62
        
        # Кнопка закрытия (справа сверху от видео)
        imagebutton:
            idle "close"        # ЗАМЕНИ на имя твоего файла (например, "close")
            hover "close_hover" # ЗАМЕНИ на имя твоего файла (например, "close_hover")
            action [
                Stop("movie"), # КРИТИЧЕСКИ ВАЖНО: останавливает видео и звук при закрытии!
                Hide("rickroll")
            ]
            # Позиционируем кнопку чуть выше и правее верхнего правого угла видео
            xalign 0.71
            yalign 0.37