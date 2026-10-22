image street_day:
    "images/street.jpg"

image kitchen:
    "images/kitchen.png"

image night_warm:
    "images/light/night_warm.jpg"
    zoom 3.0
    blend "multiply"
    alpha 0.7

image kitchen_james:
    "images/kitchen_james.jpg"
    zoom 1.25

image larsroom_night:
    "images/larsroom_dark.png"

image green_kitchen:
    "images/light/green.png"
    blend "multiply"
    alpha 0.7

image club:
    "images/club.png"
    zoom 1.5

image gym_light:
    "images/light/gym_light.png"
    blend "add"

image nighter:
    "images/light/nighter.png"
    blend "add"
    alpha 0.7

image balcony:
    im.Scale("images/balcony.jpg", 1920, 1080)

image sunset:
    "images/light/sunset.jpg"
    blend "multiply"
    alpha 0.5

image shop:
    im.Scale("images/light/shop.jpeg", 1920, 1080)
    blend "multiply"
    alpha 0.5

image balls:
    im.Scale("images/light/balls.jpg", 1920, 1080)
    blend "multiply"
    alpha 0.5

image psychodelic1:
    "psycho1"
    blend "add"
    zoom 4.2
    alpha 0.15
    

image late_night:
    "images/light/late_night.jpg"
    blend "multiply" alpha 0.5

image pink:
    "images/light/pink.jpg"
    blend "add"
    alpha 0.3

image electric:
    "images/light/electric.jpg"
    blend "multiply"
    alpha 0.4

image students:
    im.Scale("images/students.png", 1100, 1100)
    matrixcolor BrightnessMatrix(0.4)
    
image students2:
    im.Scale("images/students2.png", 1300, 1300)
    matrixcolor BrightnessMatrix(0.4)
    
layeredimage larsroom:
    always:
        "images/larsroom.jpg"
    group lighting:
        attribute pink_nightlight:
            Solid("#630f3f") alpha 0.5
            blend "multiply"
        attribute pink default:
            im.Scale("images/light/pink.jpg", 1920, 1080) alpha 0.55
            blend "multiply"
        attribute barbie:
            im.Scale("images/light/pink2.jpeg", 1920, 1080) alpha 0.75
            blend "multiply"
        attribute night:
            "images/light/night.jpg"
            blend "multiply" 
        attribute none:
            Null() 

layeredimage parking:
    always:
        "images/parking.jpg"
    group lighting:
        attribute sunrise default:
            "images/light/sunrise.jpg"
            blend "multiply"
        attribute night:
            "images/light/night.jpg"
            blend "multiply" 
        attribute none:
            Null() 

layeredimage nearhouse:
    always:
        "images/nearhouse.jpg"
    group lighting:
        attribute sunrise default:
            "images/light/sunrise.jpg"
            blend "multiply"
        attribute night:
            "images/light/night.jpg"
            blend "multiply" 
        attribute sunlight:
            Image("images/light/sun.jpg") alpha 0.5
            blend "add" 
        attribute none:
            Null() 

layeredimage street:
    always:
        "images/street.jpg"
    group lighting:
        attribute sunrise default:
            "images/light/sunrise.jpg"
            blend "multiply"
        attribute night:
            "images/light/night.jpg"
            blend "multiply" 
        attribute sun:
            "images/light/sun.jpg"
            blend "add" 
        attribute none:
            Null() 

screen smoke:
    add "smoke"
    timer 3.0 action Hide("smoke")


image wait = Movie(channel="movie", play="videos/dance_wait.mp4")
image dance_1 = Movie(channel="movie", play="videos/dance_1.mp4")
image dance_2 = Movie(channel="movie", play="videos/dance_2.mp4")
image dance_3 = Movie(channel="movie", play="videos/dance_3.mp4")


#menu
image open:
    "gui/xp_menu/open.png"
    xysize(60, 60)
image open_hover:
    im.MatrixColor("gui/xp_menu/open.png", im.matrix.tint(0.8, 0.9, 1.0)) 
    xysize(60, 60)
image play:
    "gui/xp_menu/play.png"
    xysize(60, 60)
image play_hover:
    im.MatrixColor("gui/xp_menu/play.png", im.matrix.tint(0.8, 0.9, 1.0)) 
    xysize(60, 60)
image settings:
    "gui/xp_menu/settings.png"
    xysize(60, 60)
image settings_hover:
    im.MatrixColor("gui/xp_menu/settings.png", im.matrix.tint(0.8, 0.9, 1.0)) 
    xysize(60, 60)
image gallery:
    "gui/xp_menu/gallery.png"
    xysize(60, 60)
image gallery_hover:
    im.MatrixColor("gui/xp_menu/gallery.png", im.matrix.tint(0.8, 0.9, 1.0)) 
    xysize(60, 60)
image exit:
    "gui/xp_menu/exit.png"
    xysize(60, 60)
image exit_hover:
    im.MatrixColor("gui/xp_menu/exit.png", im.matrix.tint(0.8, 0.9, 1.0)) 
    xysize(60, 60)
image close:
    "gui/xp_menu/close.png"
    xysize(30, 30)
image close_hover:
    im.MatrixColor("gui/xp_menu/close.png", im.matrix.tint(0.8, 0.9, 1.0)) 
    xysize(30, 30)

image rickroll_mp4 = Movie(play="gui/xp_menu/rickroll.mp4", size=(640, 360), loop=True)
# ==========================================
# НАСТРОЙКИ АВАТАРОК
# ==========================================
define ava_size = (60, 60)
image james_ava = im.AlphaMask(im.Scale("gui/xp_menu/james_thumbnail.png", ava_size[0], ava_size[1]), "gui/mask.png")
image kirk_ava = im.AlphaMask(im.Scale("gui/xp_menu/kirk_thumbnail.jpg", ava_size[0], ava_size[1]), "gui/mask.png")
image dave_ava = im.AlphaMask(im.Scale("gui/xp_menu/dave_thumbnail.webp", ava_size[0], ava_size[1]), "gui/mask.png")
image nick_ava = im.AlphaMask(im.Scale("gui/xp_menu/nick_thumbnail.png", ava_size[0], ava_size[1]), "gui/mask.png")
image lars_ava = im.AlphaMask(im.Scale("gui/xp_menu/lars_thumbnail.png", ava_size[0], ava_size[1]), "gui/mask.png")

