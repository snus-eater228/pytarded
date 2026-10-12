init python:
    import pickle
    import uuid
    import sys
    import os
    MAX_NOTES = 24
    BORDER = 900
    class RhythmGame:
        def __init__(self):
            self.pool_size = MAX_NOTES  # Define the size of the note pool
            self.active_notes = []  # List to track currently active notes
            self.FALL_SPEED = 20  # Pixels per second
            self.BORDER = BORDER  # Bottom of the screen height
            self.START_Y = -100  # Starting position for reinitialized notes
            self.hit_notes = []  # Track which notes have been hit
            self.is_hitting = True
            self.hurry = False

            # Загружаем карту битов
            absolute_path = f"{renpy.config.gamedir}/audio/pickled/notes"
            beatarray = pickle.load(open(absolute_path, "rb"))

            try:
                self.beatmap, self.ending_time = beatarray
            except:
                print('Unable to read audio file')
                return

            # Initialize notes based on the beatmap
            self.notes = []
            for beat in self.beatmap:
                timing = beat['time']
                position = beat['position']
                strum_time_seconds = timing / 100.0
                # Calculate initial y position based on strum time
                initial_y = self.START_Y - (self.FALL_SPEED * strum_time_seconds)
                self.notes.append({"id":uuid.uuid4(),"hit": False, 'y': initial_y, 'strum': strum_time_seconds, 'position': position})

            # Initialize the first set of active notes from the beatmap
            self.current_note_index = 0
            self.note_images = {
                1: Image("images/notes/a.png"),
                2: Image("images/notes/b.png"),
                3: Image("images/notes/c.png"),
                4: Image("images/notes/d.png"),
                5: Image("images/notes/e.png"),
                6: Image("images/notes/f.png"),
            }
            self.note_poses_x = {
                1: 1600 / 6 * 1,
                2: 1600 / 6 * 2,
                3: 1600 / 6 * 3,
                4: 1600 / 6 * 4,
                5: 1600 / 6 * 5,
                6: 1600 / 6 * 6
                }
            # Initialize the active notes pool
            self.active_notes = self.notes[:self.pool_size]  # Get the first 24 notes
            print('ready')


        def reinitialize_note(self, note):
            
            # Reset the note's position based on its initial y position
            note['y'] = self.START_Y  # Set to START_Y for immediate falling
            if note['hit'] == True:
                self.is_hitting = True
            else:
                self.is_hitting = False
            # Move to the next note in the beatmap
            self.current_note_index += 1
            if self.current_note_index < len(self.notes):
                # Update the note's position and type from the beatmap
                next_beat = self.notes[self.current_note_index]
                note['position'] = next_beat['position']
                note['strum'] = next_beat['strum']
                note["hit"]=False
                note['id']=next_beat['id']
                # Set the new y position to start falling immediately
                note['y'] = self.START_Y  # Set to START_Y for immediate falling
            else:
                # If there are no more notes left in the beatmap, you can stop or loop
                return

        def get_active_notes_data(self):
            # Prepare data for rendering active notes
            return [
                (self.note_images[note['position']], (self.note_poses_x[note['position']], note['y']), note['id'], note['hit']) 
                for note in self.active_notes if note['position'] is not None
            ]
        def update_active_notes(self):
            # Update the position of each active note
            for note in self.active_notes:
                note['y'] += self.FALL_SPEED
                
                # Check if the note has fallen off the screen
                if note['y'] >= self.BORDER:
                    self.reinitialize_note(note)

        def find_closest_note_to_border(self, position):
            closest_note = None
            closest_distance = float('inf')  # Start with an infinitely large distance

            for note in self.active_notes:
                if note['position'] == position and note['y'] < self.BORDER:
                    distance_to_border = self.BORDER - note['y']
                    if distance_to_border < closest_distance and note['hit'] == False:
                        closest_distance = distance_to_border
                        closest_note = note
                    elif distance_to_border < closest_distance and note['hit'] == True:
                        renpy.play("audio/sounds/chord.mp3", channel="sound")
                        self.hurry = True


            return closest_note
                        
        def hit_note_at_position(self, position):
            closest_note = self.find_closest_note_to_border(position)
            #print(closest_note)
            if closest_note:
                closest_note['hit'] =True
                self.hurry = False
                self.hit_notes.append(closest_note['id'])  # Mark the note as hit

transform update_note_pos(note_pos):
    xpos int(note_pos[0])
    ypos int(note_pos[1])
    


screen rhythm_game(game):
    zorder 10
    default mul = 0
    default idx = 0
    default notes = [i for i in range(0, MAX_NOTES)]
    default note = None
    timer 0.016 repeat True action Function(game.update_active_notes) 
    window:
        style "default"
        add "images/club.png"
        if not game.is_hitting:
            add Movie(play="videos/dance_wait.mp4")
        else:
            default chosen_movie = renpy.random.choice([Movie(play="videos/dance_1.mp4"), Movie(play="videos/dance_3.mp4"), Movie(play="videos/dance_2.mp4")])
            add chosen_movie
        text "нажимай на цифры на клавиатуре вовремя лошок!!" xalign 0.5 yalign 0.05 color "#fff" size 40
        # Отображаем активные ноты
        for note_image, note_pos, note_id, note_hit in game.get_active_notes_data():
            if note_hit:
                add im.Scale("images/notes/pressed.png", 50, 50) at update_note_pos(note_pos)
            else:
                add im.Scale(note_image, 50, 50) at update_note_pos(note_pos)
        if game.hurry:
                text "по очереди жми на клаву дура не все разом" xalign 0.5 yalign 0.1 size 40 color "#ff0000"


        key "1" action Function(game.hit_note_at_position, 1)
        key "2" action Function(game.hit_note_at_position, 2)
        key "3" action Function(game.hit_note_at_position, 3)
        key "4" action Function(game.hit_note_at_position, 4)
        key "5" action Function(game.hit_note_at_position, 5)
        key "6" action Function(game.hit_note_at_position, 6)
                    

