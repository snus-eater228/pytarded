label dance_game:
    scene club with dissolve

    # Прячем UI новеллы
    window hide
    # ЗАМЕНИ "side_menu" НА РЕАЛЬНОЕ ИМЯ ТВОЕГО ЭКРАНА БОКОВОГО МЕНЮ
    $ renpy.hide_screen("quick_menu")
    $ rhythm_game = RhythmGame()
    $ rhythm_game.start()
    show dancer at dance_floor
    show expression rhythm_game at truecenter
    show screen rhythm_ui()
    $ renpy.play("audio/music/black.ogg", "music")

    $ renpy.pause(225, hard=True)
    $ rhythm_game.stop()
    $ renpy.music.stop()
    hide expression rhythm_game
    hide screen rhythm_ui
    hide dancer

    # Возвращаем UI
    $ renpy.show_screen("quick_menu")  # ← то же имя

    "Игра окончена! Твой счет: [rhythm_game.score]. Максимальное комбо: [rhythm_game.max_combo]"

    return