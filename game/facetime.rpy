default facetime_location = None
default facetime_character = None
default facetime_emotion = None
default facetime_light = None
default name_changed = False


transform rgb_glitch:
    parallel:
        linear 0.03 xoffset -3
        linear 0.03 xoffset 3
        repeat
    parallel:
        linear 0.02 yoffset 2
        linear 0.02 yoffset -2
        repeat

screen facetime:
    add AlphaMask(Transform(store.facetime_location, crop=(550, 0, 407, 800)), "gui/phone_mask.png")  xalign 0.9 yalign 0.9
    add AlphaMask(Transform("images/[facetime_character] [facetime_emotion].png", crop=(0, -300, 407, 800)), "gui/phone_mask.png") xalign 0.9 yalign 0.9
    add AlphaMask(Transform(store.facetime_light, crop=(600, 0, 407, 800)), "gui/phone_mask.png") blend "multiply" alpha 0.7 xalign 0.9 yalign 0.9
    
    add "gui/facetime.png" zoom 0.63 xalign 0.9 yalign 0.9
    if store.facetime_character == "james" and not store.name_changed:
        text "Jaymz (Senior Python Developer,\n Machine Learning, Robotics)" color "#fff" size 18 xalign 0.88 yalign 0.31
    elif store.facetime_character == "james" and store.name_changed:
        text "джейми траходром" color "#fff" size 16 xalign 0.8 yalign 0.3
    if store.facetime_character == "dave":
        text "шумахер ебаный" color "#fff" size 16 xalign 0.8 yalign 0.3
    if store.facetime_character == "kirk":
        text "киркуша вайбуша" color "#fff" size 16 xalign 0.8 yalign 0.3
    
    if store.facetime_character == "james":
        add "gui/james_facetime_icon.png" zoom 0.125 xalign 0.75 yalign 0.32
    
    

init python:

    def show_facetime(name, emotion):
        renpy.show(f"{name}_{emotion}")
        
        if facetime_active and facetime_character == name:
            store.facetime_emotion = emotion
            renpy.restart_interaction()