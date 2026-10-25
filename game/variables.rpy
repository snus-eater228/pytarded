init python:
    renpy.config.hard_rollback_limit = 5
    def my_label_callback(name, abnormal):
        # Записываем имя текущего лейбла в глобальную переменную store.current_label
        store.current_label = name
    config.label_callback = my_label_callback

default current_label = "start"
default will = Stat("will")
default respect = Stat("respect")
default brain_lars = Stat("brain_lars")
default brain_dave = Stat("brain_dave")
default nick_rel = LoveVariable("nick")
default kirk_rel = LoveVariable("kirk")
default james_rel = LoveVariable("james")
default hetstaine = LoveVariable("james", "dave")
default dave_rel = LoveVariable("dave")
default branch = 0
default urok1 = False
default dave_zakat_photo = False

default nvl_mode = "board"

default dave_ur = False
default dz_1 = False

default ls = ""

default persistent.gallery = None
#input
default inpval = ""

default chapters = [
("вашей маме зять не нужен? ;D", (140, 81), "1"), 
("кумароведение и кримпай ;-)", (585, 324), "2"),
("вездесущий пожилой жмых :P", (207, 729), "3"), 
("глава 4", (606, 1017), "4"),
("глава 5", (1000, 690), "5"),
("глава 6", (1300, 190), "6"),
("глава 7", (1730, 450), "7"),
("глава 8", (1800, 850), "8"),
("глава 9", (2200, 300), "9"),
("глава 10", (2000, 700), "10")
]

default persistent.progress = "1"
default rhythm_game = None
default latest_snapshot_qr = ""
default current_checkpoint = ""