default speed_x = 5
default speed_y = 5
default pos_x = 270
default pos_y = 0

init python:
    def _get(file_name, ext):
        return 'gui/' + file_name + '.' + ext 

image bg= _get("main", "jpg")

image sign:
    At("gui/sign.png", PathMotion(adjusted_bounce_path, 100.0, repeat=True, bounce=False, sizes=((800,300))))
    xsize 800
    ysize 300

        



screen main_menu_animation():
    tag menu
    add "bg"
    add "sign" blend "add"
    vbox:
        xalign 0.05
        yalign 0.5
        xsize 300
        spacing 30
        imagebutton:
            ypos 30
            xsize 150
            ysize 150
            xalign 0.5
            idle im.Scale("gui/key_start.png", 150,150)
            hover im.Scale("gui/key_start_pressed.png",150,150)
            action Show("premenu")
        imagebutton:
            xsize 150
            ysize 150
            xalign 0.5
            yalign 0.5
            idle im.Scale("gui/key_open.png", 150,150)
            hover im.Scale("gui/key_open_pressed.png",150,150)
            action ShowMenu('load')
        imagebutton:
            xsize 150
            ysize 150
            xalign 0.5
            yalign 0.5
            idle im.Scale("gui/key_config.png", 150,150)
            hover im.Scale("gui/key_config_pressed.png",150,150)
            action ShowMenu("preferences")
        imagebutton:
            xsize 150
            ysize 150
            xalign 0.5
            yalign 0.5
            idle im.Scale("gui/key_help.png", 150,150)
            hover im.Scale("gui/key_help_pressed.png",150,150)
            action ShowMenu("help")
        imagebutton:
            xsize 150
            ysize 150
            xalign 0.5
            yalign 0.5
            idle im.Scale("gui/gallery.png", 150,150)
            hover im.Scale("gui/gallery_pressed.png",150,150)
            action ShowMenu('gallery')
        imagebutton:
            xsize 150
            ysize 150
            xalign 0.5
            yalign 0.5
            idle im.Scale("gui/key_exit.png", 150,150)
            hover im.Scale("gui/key_exit_pressed.png",150,150)
            action Quit()
