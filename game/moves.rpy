transform move_x(x, speed = 0.5):
    yalign 1.0
    linear speed xalign x
    repeat False

transform move_x_from(f, x, speed = 0.5):
    yalign 1.0
    xalign f
    linear speed xalign x
    repeat False

transform dance_floor:
    xalign 0.25
    yalign 0.4
    zoom 0.5

transform my_left:
    xalign 0.33
    yalign 1.0

transform my_right:
    xalign 0.66
    yalign 1.0

transform my_left_left:
    xalign 0.15
    yalign 1.0

transform flip:
    xzoom -1.0

transform jumping:
    yanchor 1.0 ypos 1.0
    easeout 0.3 ypos 0.8
    easein 0.3 ypos 1.0
    repeat

transform ver_right:
    xalign 1.1
    yalign 1.0
    