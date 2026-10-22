define james_zoom__koef = 0.79
define dave_zoom_koef = 0.77
define lars_zoom__koef = 0.8
define kirk_zoom_koef = 0.72
define nick_zoom__koef = 0.7
define girl_zoom_koef = 0.7

image dave think = At('dave think demo', sprite_highlight('dave'))
image dave think demo:
    zoom dave_zoom_koef
    "images/dave new.png"
image dave side1 = At('dave side1 demo', sprite_highlight('dave'))
image dave side1 demo:
    zoom dave_zoom_koef
    "images/dave new.png"
image dave side2 = At('dave side2 demo', sprite_highlight('dave'))
image dave side2 demo:
    zoom dave_zoom_koef
    "images/dave new.png"
image dave angry = At('dave angry demo', sprite_highlight('dave'))
image dave angry demo:
    zoom dave_zoom_koef
    "images/dave new.png"
image dave sad = At('dave sad demo', sprite_highlight('dave'))
image dave sad demo:
    zoom dave_zoom_koef
    "images/dave new.png"
image dave smile = At('dave smile demo', sprite_highlight('dave'))
image dave smile demo:
    zoom dave_zoom_koef
    "images/dave new.png"
image dave pink normal = At('dave pink normal demo', sprite_highlight('dave'))
image dave pink normal demo:
    zoom dave_zoom_koef
    "images/dave new.png"
image dave pink smile = At('dave pink smile demo', sprite_highlight('dave'))
image dave pink smile demo:
    zoom dave_zoom_koef
    "images/dave new.png"
image dave pink sad = At('dave pink sad demo', sprite_highlight('dave'))
image dave pink sad demo:
    zoom dave_zoom_koef
    "images/dave new.png"
image dave pink happy = At('dave pink happy demo', sprite_highlight('dave'))
image dave pink happy demo:
    zoom dave_zoom_koef
    At("images/dave new.png", flip)
image dave blue normal = At('dave blue normal demo', sprite_highlight('dave'))
image dave blue normal demo:
    zoom dave_zoom_koef
    "images/dave new.png"
image dave blue irritated = At('dave blue irritated demo', sprite_highlight('dave'))
image dave blue irritated demo:
    zoom dave_zoom_koef
    "images/dave new.png"

image james blush = At("james blush demo", sprite_highlight('james'))
image james blush demo:
    "images/james blush.png"
    zoom james_zoom__koef
image james normal = At("james normal demo", sprite_highlight('james'))
image james normal demo:
    "images/james normal.png"
    zoom james_zoom__koef
image james smile = At("james smile demo", sprite_highlight('james'))
image james smile demo:
    "images/james smile.png"
    zoom james_zoom__koef
image james sad = At("james sad demo", sprite_highlight('james'))
image james sad demo:
    "images/james sad.png"
    zoom james_zoom__koef
image james naked normal = At("james naked normal demo", sprite_highlight('james'))
image james naked normal demo:
    "images/james naked normal.png"
    zoom james_zoom__koef
image james naked blush = At("james naked blush demo", sprite_highlight('james'))
image james naked blush demo:
    "images/james naked blush.png"
    zoom james_zoom__koef

image lars blush naked = At("lars blush naked demo", sprite_highlight('lars'))
image lars blush naked demo:
    "images/lars blush naked.png"
    zoom lars_zoom__koef
image lars angry = At("lars angry demo", sprite_highlight('lars'))
image lars angry demo:
    "images/lars new.png"
    zoom lars_zoom__koef
image lars cow greeting = At("lars cow greeting demo", sprite_highlight('lars'))
image lars cow greeting demo:
    "images/lars new.png"
    zoom lars_zoom__koef
image lars please = At("lars please demo", sprite_highlight('lars'))
image lars please demo:
    "images/lars new.png"
    zoom lars_zoom__koef
image lars test = At("lars test demo", sprite_highlight('lars'))
image lars test demo:
    "images/lars new.png"
    zoom 2
image lars cow offense = At("lars cow offense demo", sprite_highlight('lars'))
image lars cow offense demo:
    "images/lars new.png"
    zoom lars_zoom__koef
image lars normal = At("lars normal demo", sprite_highlight('lars'))
image lars normal demo:
    "images/lars new.png"
    zoom lars_zoom__koef
image lars happy naked = At("lars happy naked demo", sprite_highlight('lars'))
image lars happy naked demo:
    "images/lars new.png"
    zoom lars_zoom__koef
image lars irritated = At("lars irritated demo", sprite_highlight('lars'))
image lars irritated demo:
    "images/lars new.png"
    zoom lars_zoom__koef
image lars blush naked = At("lars blush naked demo", sprite_highlight('lars'))
image lars blush naked demo:
    "images/lars new.png"
    zoom lars_zoom__koef
image lars smile = At("lars smile demo", sprite_highlight('lars'))
image lars smile demo:
    "images/lars new.png"
    zoom lars_zoom__koef
image lars sad = At("lars sad demo", sprite_highlight('lars'))
image lars sad demo:
    "images/lars new.png"
    zoom lars_zoom__koef
image lars yellow demo:
    "images/lars new.png"
    zoom lars_zoom__koef
image lars yellow = At("lars yellow demo", sprite_highlight('lars'))

image nick sad = At("nick sad demo", sprite_highlight('nick'))
image nick sad demo:
    "images/nick sad.png"
    zoom nick_zoom__koef
image nick side = At("nick side demo", sprite_highlight('nick'))
image nick side demo:
    "images/nick side.png"
    zoom nick_zoom__koef
image nick normal = At("nick normal demo", sprite_highlight('nick'))
image nick normal demo:
    "images/nick normal.png"
    zoom nick_zoom__koef
image nick smile = At("nick smile demo", sprite_highlight('nick'))
image nick smile demo:
    "images/nick smile.png"
    zoom nick_zoom__koef

image kirk sad = At("kirk sad demo", sprite_highlight('kirk'))
image kirk sad demo:
    "images/kirk sad.png"
    zoom kirk_zoom_koef
image kirk normal = At("kirk normal demo", sprite_highlight('kirk'))
image kirk normal demo:
    "images/kirk normal.png"
    zoom kirk_zoom_koef

image gerard normal = At("gerard normal demo", sprite_highlight("gerard"))
image gerard normal demo:
    "images/gerard normal.png"
    zoom girl_zoom_koef

image gerard side = At("gerard side demo", sprite_highlight("gerard"))
image gerard side demo:
    "images/gerard side.png"
    zoom girl_zoom_koef


image jason normal = At("jason normal demo", sprite_highlight("jason"))
image jason normal demo:
    "images/jason normal.png"
    zoom 0.81

image jason blush = At("jason blush demo", sprite_highlight("jason"))
image jason blush demo:
    "images/jason blush.png"
    zoom 0.81


define narrator = Character(None,window_background="gui/textboxes/narrator.png")
define d = Character("дйв", color="#3a0a0a", image="dave", window_background="gui/textboxes/dave.png", callback=name_callback, cb_name="dave")
define l = Character("срал улей", color="#c45e9d", image="lars", window_background="gui/textboxes/lars.png",callback=name_callback, cb_name="lars")
define j = Character("джйм", color="#bac45e", image="james", window_background="gui/textboxes/james.png",callback=name_callback, cb_name="james")
define n = Character("никотин менза", color="#575757", image="nick", window_background="gui/textboxes/neutral.png",callback=name_callback, cb_name="nick")
define k = Character("кириешка", color="#201212", image="kirk", window_background="gui/textboxes/neutral.png",callback=name_callback, cb_name="kirk")
define board = Character(kind=nvl, what_color="#fff", what_font="gui/tahoma.ttf", callback=switch_mode, cb_name = "board")
define computer = Character(kind=nvl, what_color="#191820", what_font="gui/tahoma.ttf",  callback=switch_mode, cb_name = "computer")
define computer_print = Character(kind=nvl, what_color="#acacac", what_font="gui/clacon2.ttf",  callback=switch_mode, cb_name = "print")
define ge = Character("1000-7", color="#868686", image="gerard", window_background="gui/textboxes/neutral.png",callback=name_callback, cb_name="gerard")
define js = Character("json", color="#b29d85", image="jason", window_background="gui/textboxes/neutral.png",callback=name_callback, cb_name="jason")
