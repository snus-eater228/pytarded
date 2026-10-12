screen premenu():
    modal True
    viewport:
        draggable True
        mousewheel True
        child_size(2944, 1656)
        scrollbars "both"
        add "images/viewport.jpg"
        #imagebutton xpos 200 ypos 100 idle im.Scale("images/chapters/1.png", 300, 300) hover im.Scale("images/chapters/clicked.png", 300, 300) action Start()
        #imagebutton xpos 500 ypos 300 idle im.Scale("images/chapters/unknown.png", 300, 300) action Notify("Этот эпизод ещё не \nвышел...")
        for i in range(len(chapters)-1):
            if  chapters[i][2] == persistent.progress:
                add "gui/chapters/opened.png" xpos chapters[i][1][0] ypos chapters[i][1][1] 
                imagebutton xpos chapters[i][1][0] ypos chapters[i][1][1] idle AlphaMask(Transform(Transform(f"gui/chapters/ch{i+1}.png", size=(500,500)), crop=(0,10,470,410)), "gui/chapters/placeholder.png") hover "gui/chapters/clicked.png" action Start()
            elif chapters[i+1][2] == persistent.progress:
                add "gui/chapters/passed.png" xpos chapters[i][1][0] ypos chapters[i][1][1]
                add AlphaMask(Transform(Transform(f"gui/chapters/ch{i+1}.png", size=(500,500)), crop=(0,10,470,410)), "gui/chapters/placeholder.png") xpos chapters[i][1][0] ypos chapters[i][1][1]
            else:
                add "gui/chapters/current.png" xpos chapters[i][1][0] ypos chapters[i][1][1] 
                text "???" xpos chapters[i][1][0]+230 ypos chapters[i][1][1]+170 size 60 color "#fff" font "gui/Veles.ttf"
            text chapters[i][2] xpos chapters[i][1][0]+90 ypos chapters[i][1][1]+290 size 50 color "#fff" font "gui/Veles.ttf"



        
        