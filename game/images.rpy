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

image gym_light:
    "images/light/gym_light.png"
    blend "add"

image nighter:
    "images/light/nighter.png"
    blend "add"
    alpha 0.7

image balcony:
    im.Scale("images/balcony.jpg", 1920, 1080)

image day_sun:
    "images/light/sun.jpg"
    blend "add"
    alpha 0.3

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
    
image sunrise:
    "images/light/sunrise.jpg"
    blend "multiply"

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
    
    

screen smoke:
    add "smoke"
    timer 3.0 action Hide("smoke")


image wait = Movie(channel="movie", play="videos/dance_wait.mp4")
image dance_1 = Movie(channel="movie", play="videos/dance_1.mp4")
image dance_2 = Movie(channel="movie", play="videos/dance_2.mp4")
image dance_3 = Movie(channel="movie", play="videos/dance_3.mp4")