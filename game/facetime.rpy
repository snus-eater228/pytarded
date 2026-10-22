screen facetime_screen(caller, location, light=None):

    $ phone_x = 0.9
    $ phone_y = 0.9
    $ mask = "gui/phone_mask.png"
    $ current_lit = getattr(store, f"lit_{store.current_light.value}", None)

    # 1. Создаем персонажа с освещением
    $ char_base = AlphaMask(Transform(f"{caller} {facetime_emotion}", crop=(0, -300, 407, 800)), mask)
    if current_lit:
        $ char_displayable = At(char_base, current_lit)
    else:
        $ char_displayable = char_base

    # 2. Создаем фон
    $ bg_displayable = AlphaMask(Transform(location, crop=(550, 0, 407, 800)), mask)

    # 3. ОБЪЕДИНЯЕМ их в один контейнер. Теперь это единое "видео"
    $ phone_video_content = Fixed(bg_displayable, char_displayable,xsize=407, 
        ysize=800)

    # 4. Применяем глитч ко всему видео целиком!
    if facetime_heavy_glitch:
        add At(phone_video_content, glitch_heavy_fx) xalign phone_x yalign phone_y
        # АВТОМАТИЧЕСКИЙ ТАЙМЕР: выключает тяжелый глитч через 1.5 секунды
        timer 1.5 action SetVariable("facetime_heavy_glitch", False)
    else:
        add At(phone_video_content, glitch_subtle_fx) xalign phone_x yalign phone_y

    # 5. Дополнительный свет (поверх видео, но под рамкой)
    if light:
        add AlphaMask(Transform(light, crop=(600, 0, 407, 800)), mask) blend "multiply" alpha 0.7 xalign phone_x yalign phone_y
    
    # 6. Рамка и UI (НИКОГДА не глитчатся, лежат поверх)
    add "gui/facetime.png" zoom 0.63 xalign 0.965 yalign 1.125
    
    if caller == "james" and not store.name_changed:
        add "gui/james_facetime_icon.png" zoom 0.125 xalign 0.75 yalign 0.32
        text "Jaymz (Senior Python Developer,\n Machine Learning, Robotics)" color "#fff" size 18 xalign 0.88 yalign 0.31
    elif caller == "james" and store.name_changed:
        add "gui/james_facetime_icon.png" zoom 0.125 xalign 0.75 yalign 0.32
        text "джейми траходром" color "#fff" size 16 xalign 0.8 yalign 0.3
    elif caller == "dave":
        add "dave_ava" zoom 1.5 xalign 0.754 yalign 0.315
        text "шумахер героиновый" color "#fff" size 16 xalign 0.83 yalign 0.32
    elif caller == "kirk":
        text "киркуша вайбуша" color "#fff" size 16 xalign 0.8 yalign 0.3
        add "gui/james_facetime_icon.png" zoom 0.125 xalign 0.75 yalign 0.32
init python:
    def start_facetime(caller, emotion, location, light=None):
        store.is_facetime = True
        store.facetime_caller = caller
        store.facetime_location = location
        store.facetime_light = light
        store.facetime_emotion = emotion 
        store.facetime_heavy_glitch = False
        renpy.show_screen("facetime_screen", caller=caller, location=location, light=light)

    def end_facetime():
        store.is_facetime = False
        store.facetime_caller = ""
        store.facetime_location = ""
        store.facetime_light = None
        store.facetime_emotion = ""
        store.facetime_heavy_glitch = False
        renpy.hide_screen("facetime_screen")

    # Просто включаем флаг. Таймер в экране сам выключит его через 1.5 сек.
    def trigger_heavy_glitch():
        store.facetime_heavy_glitch = True
        renpy.restart_interaction() # Мгновенно обновляет экран