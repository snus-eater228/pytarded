init python:
    import os
    import pygame
    import json
    import math
    import random
    # === АНИМАЦИИ ТАНЦА ===
    def _build_dance_animation(prefix, delay=0.22):
        """Сканирует images/dance/{prefix}1.png, {prefix}2.png, ... и собирает Animation."""
        dance_dir = os.path.join(config.gamedir, "images", "dance")
        if not os.path.isdir(dance_dir):
            return Solid("#ff00ff", xsize=300, ysize=400)
        frames = []
        i = 1
        while True:
            filename = "{}{}.png".format(prefix, i)
            full_path = os.path.join(dance_dir, filename)
            if not os.path.exists(full_path):
                break
            frames.append("dance/{}".format(filename))
            frames.append(delay)
            i += 1
        if not frames:
            return Solid("#ff00ff", xsize=300, ysize=400)
        return Animation(*frames)

    dance_normal_anim = _build_dance_animation("r")
    dance_stumble_anim = _build_dance_animation("st")
    dance_raskolbas_anim = _build_dance_animation("k")

    # === БЛОКИРОВКА КЛАВИАТУРЫ ===
    saved_renpy_keymap = {}

    def lock_renpy_keyboard():
        renpy.clear_keymap_cache()
        global saved_renpy_keymap
        if saved_renpy_keymap:
            return
        saved_renpy_keymap = {}
        for k in list(config.keymap.keys()):
            v = config.keymap[k]
            saved_renpy_keymap[k] = list(v) if v else []
            config.keymap[k].clear()
        renpy.block_rollback()

    def unlock_renpy_keyboard():
        global saved_renpy_keymap
        renpy.clear_keymap_cache()
        if saved_renpy_keymap:
            config.keymap = saved_renpy_keymap
            saved_renpy_keymap = {}
    def end_rhythm_game():
        """Останавливает ритм-игру, музыку, восстанавливает keymap, обрывает паузу."""
        rg = getattr(renpy.store, 'rhythm_game', None)
        if rg is not None and rg.is_playing:
            rg.stop()
        renpy.music.stop()
        # Обрывает текущий renpy.pause() и возвращает None
        renpy.end_interaction(None)
    # === ЧАСТИЦЫ И ВСПЫШКИ ===
    class Particle(python_object):
        __slots__ = ('x', 'y', 'vx', 'vy', 'life', 'max_life', 'color', 'size')
        def __init__(self, x, y, color, size_range=(2, 6), speed_range=(120, 380)):
            self.x = float(x)
            self.y = float(y)
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(*speed_range)
            self.vx = math.cos(angle) * speed
            self.vy = math.sin(angle) * speed
            self.life = 1.0
            self.max_life = random.uniform(0.4, 0.9)
            self.color = color
            self.size = random.uniform(*size_range)
        def update(self, dt):
            self.x += self.vx * dt
            self.y += self.vy * dt
            self.vy += 180 * dt
            self.vx *= 0.92
            self.vy *= 0.92
            self.life -= dt / self.max_life
            return self.life > 0
        def draw(self, surface):
            if self.life <= 0: return
            alpha = int(255 * (self.life ** 0.5))
            size = max(1, int(self.size * (0.4 + 0.6 * self.life)))
            pygame.draw.circle(surface, (*self.color, alpha), (int(self.x), int(self.y)), size)

    class Flash(python_object):
        __slots__ = ('x', 'y', 'color', 'radius', 'max_radius', 'life', 'max_life')
        def __init__(self, x, y, color, max_radius=100):
            self.x = float(x)
            self.y = float(y)
            self.color = color
            self.radius = 15.0
            self.max_radius = float(max_radius)
            self.life = 1.0
            self.max_life = 0.35
        def update(self, dt):
            self.radius += (self.max_radius - self.radius) * dt * 10
            self.life -= dt / self.max_life
            return self.life > 0
        def draw(self, surface):
            if self.life <= 0: return
            alpha = int(255 * (self.life ** 1.5))
            r = int(self.radius)
            if r <= 0 or alpha <= 0: return
            f_surf = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
            pygame.draw.circle(f_surf, (*self.color, alpha), (r, r), r)
            surface.blit(f_surf, (int(self.x) - r, int(self.y) - r), special_flags=pygame.BLEND_RGBA_ADD)

    # === НОТА ===
    class Note:
        def __init__(self, spawn_time, lane, hit_time):
            self.spawn_time = spawn_time
            self.lane = lane
            self.hit_time = hit_time
            self.y = 0.0
            self.active = True
            self.is_hit = False
            self.has_missed = False
            self.hit_progress = 0.0
            self._particles_spawned = False
            self.keep_at_low_diff = True
        def update(self, current_time, fall_duration, dt):
            if self.is_hit:
                self.hit_progress += dt * 3.5
                if self.hit_progress >= 1.0:
                    self.active = False
            else:
                elapsed = current_time - self.spawn_time
                self.y = elapsed / fall_duration
                self.y = max(0.0, min(1.2, self.y))
                if self.y > 1.2:
                    self.active = False

    # === РИТМ-ИГРА ===
    class RhythmGame(renpy.Displayable):
        COMBO_X10 = 5
        COMBO_X20 = 10
        COMBO_RASKOLBAS = 15
        LANE_KEYS = ['D', 'F', 'J', 'K']  # НОВОЕ: буквы подсказок

        def __init__(self, **kwargs):
            super(RhythmGame, self).__init__(**kwargs)
            with open(renpy.loader.transfn("black.json"), "r", encoding="utf-8") as f:
                self.notes_data = json.load(f)
            self.notes = []

            self.base_fall_duration = 1.5
            self.lanes = 4
            self.note_radius = 35

            self.pre_hit_end = 0.35
            self.hit_center = 0.45
            self.missed_start = 0.55

            self.lane_colors = [(255, 80, 80), (255, 220, 80), (80, 255, 120), (80, 140, 255)]
            self.key_map = {pygame.K_d: 0, pygame.K_f: 1, pygame.K_j: 2, pygame.K_k: 3}
            self.unicode_map = {'d': 0, 'в': 0, 'В': 0, 'f': 1, 'а': 1, 'А': 1, 'j': 2, 'о': 2, 'О': 2, 'k': 3, 'л': 3, 'Л': 3}

            self.game_time = 0.0
            self.current_note_index = 0
            self.is_playing = False
            self.last_st = None

            self.score = 0
            self.combo = 0
            self.max_combo = 0
            self.particles = []
            self.flashes = []

            # НОВОЕ: таймеры визуального нажатия клавиш
            self.lane_press_timer = [0.0, 0.0, 0.0, 0.0]
            self.PRESS_DURATION = 0.2  # 200мс отклик

            self.combo_milestone = None
            self.milestone_timer = 0.0

            self._load_notes()

        def _load_notes(self):
            pattern = [True] * 15 + [False] * 5
            rng = random.Random(42)
            rng.shuffle(pattern)
            self.notes = []
            for i, note_data in enumerate(self.notes_data):
                note = Note(note_data["time"], note_data["lane"], note_data["hit_time"])
                note.keep_at_low_diff = pattern[i % 20]
                self.notes.append(note)

        def get_difficulty_stats(self):
            if self.combo >= self.COMBO_RASKOLBAS:
                return {"points": 30, "tolerance": 0.04, "state": "ultra_raskolbas"}
            elif self.combo >= self.COMBO_X20:
                return {"points": 15, "tolerance": 0.06, "state": "combo_x20"}
            elif self.combo >= self.COMBO_X10:
                return {"points": 8, "tolerance": 0.08, "state": "combo_x10"}
            else:
                return {"points": 2, "tolerance": 0.12, "state": "normal"}

        def render(self, width, height, st, at):
            surface = pygame.Surface((width, height), pygame.SRCALPHA)
            dt = (st - self.last_st) if self.last_st is not None else 0.0
            self.last_st = st

            if self.is_playing:
                self.game_time += dt
                # НОВОЕ: обновляем таймеры нажатия клавиш
                for i in range(self.lanes):
                    if self.lane_press_timer[i] > 0:
                        self.lane_press_timer[i] = max(0.0, self.lane_press_timer[i] - dt)
                
                self._draw_stained_glass(surface, width, height)
                self._draw_hit_zone(surface, width, height)  # ИЗМЕНЕНО: мягкая линия
                self._spawn_notes()
                self._update_and_draw_notes(surface, width, height, dt)
                self._update_and_draw_flashes(surface, dt)
                self._update_and_draw_particles(surface, dt)

                if self.combo_milestone is not None:
                    self.milestone_timer -= dt
                    if self.milestone_timer <= 0:
                        self.combo_milestone = None
                        self.milestone_timer = 0.0
                        renpy.restart_interaction()

            render = renpy.Render(width, height)
            render.blit(surface, (0, 0))
            renpy.redraw(self, 0)
            return render

        def _draw_stained_glass(self, surface, width, height):
            lane_width = width // self.lanes
            for i in range(self.lanes):
                glass = pygame.Surface((lane_width, height), pygame.SRCALPHA)
                glass.fill((*self.lane_colors[i], 40))
                surface.blit(glass, (i * lane_width, 0))

        # ИЗМЕНЕНО: мягкая широкая линия попадания + свечение
        def _draw_hit_zone(self, surface, width, height):
            y = int(self.hit_center * height)

            # Мягкое свечение вверх/вниз от линии (аддитивное)
            glow_h = 15
            glow_surf = pygame.Surface((width, glow_h * 2), pygame.SRCALPHA)
            for i in range(glow_h, 0, -1):
                t = i / glow_h
                alpha = int(28 * (1.0 - t) ** 2)
                if alpha <= 0: continue
                pygame.draw.rect(glow_surf, (255, 255, 255, alpha),
                                (0, glow_h - i, width, 1))
                pygame.draw.rect(glow_surf, (255, 255, 255, alpha),
                                (0, glow_h + i - 1, width, 1))
            surface.blit(glow_surf, (0, y - glow_h), special_flags=pygame.BLEND_RGBA_ADD)

            # Сама линия попадания — 8px с градиентом (ярче в центре)
            line_h = 8
            for i in range(line_h):
                t = abs(i - line_h / 2 + 0.5) / (line_h / 2)  # 0 центр, 1 края
                alpha = int(180 * (1.0 - t * 0.55))
                pygame.draw.rect(surface, (255, 255, 255, alpha),
                                (0, y - line_h // 2 + i, width, 1))

            # Цветные акценты по lane (тонкие, 2px, по центру линии)
            lane_width = width // self.lanes
            for i in range(self.lanes):
                pygame.draw.rect(surface, (*self.lane_colors[i], 230),
                                (i * lane_width + 8, y - 1,lane_width - 16, 2))

            # Границы активной зоны
            pre_y = int(self.pre_hit_end * height)
            miss_y = int(self.missed_start * height)
            for line_y in (pre_y, miss_y):
                pygame.draw.line(surface, (255, 255, 255, 50), (0, line_y), (width, line_y), 1)
        def _spawn_notes(self):
            is_raskolbas = self.combo >= self.COMBO_RASKOLBAS
            while (self.current_note_index < len(self.notes) and self.notes[self.current_note_index].spawn_time <= self.game_time):
                note = self.notes[self.current_note_index]
                if not is_raskolbas and not note.keep_at_low_diff:
                    note.active = False
                self.current_note_index += 1

        def _update_and_draw_notes(self, surface, width, height, dt):
            lane_width = width // self.lanes
            stats = self.get_difficulty_stats()

            for note in self.notes:
                if not note.active: continue

                note.update(self.game_time, self.base_fall_duration, dt)

                if not note.is_hit and not note.has_missed and note.y > self.missed_start:
                    note.has_missed = True
                    self.combo = 0
                    renpy.store.char_dance_state = "stumble"
                    global stumble_timer
                    stumble_timer = 0.0
                    renpy.restart_interaction()

                if not note.active: continue

                center_x = note.lane * lane_width + lane_width // 2
                center_y = int(note.y * height)

                if note.is_hit:
                    if not note._particles_spawned:
                        self._spawn_hit_particles(center_x, center_y, note.lane)
                        note._particles_spawned = True
                    continue

                self._draw_note(surface, center_x, center_y, note, stats)

        def _draw_note(self, surface, x, y, note, stats):
            lane_color = self.lane_colors[note.lane]

            if note.has_missed:
                progress = min(1.0, (note.y - self.missed_start) / (1.2 - self.missed_start))
                alpha = int(180 * (1.0 - progress))
                if alpha <= 0: return
                pygame.draw.circle(surface, (120, 120, 120, alpha), (x, y), self.note_radius)
                return

            dist_to_center = abs(note.y - self.hit_center)
            norm_dist = min(dist_to_center / stats["tolerance"], 1.0)
            glow_factor = max(0.0, 1.0 - norm_dist) ** 1.5

            in_active_zone = self.pre_hit_end <= note.y <= self.missed_start
            pulse = 1.0 + 0.15 * math.sin(self.game_time * 12 + note.lane * 1.5) if in_active_zone else 1.0

            if glow_factor > 0.05:
                glow_radius = int(self.note_radius * (1.5 + glow_factor * 1.2) * pulse)
                layers = [
                    (glow_radius, (255, 100, 50), 0.18),
                    (int(glow_radius * 0.7), (255, 200, 100), 0.35),
                    (int(glow_radius * 0.45), (255, 255, 200), 0.55),
                ]
                for r, color, alpha_mult in layers:
                    if r <= 0: continue
                    a = int(255 * glow_factor * alpha_mult)
                    if a <= 0: continue
                    g_surf = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
                    pygame.draw.circle(g_surf, (*color, a), (r, r), r)
                    surface.blit(g_surf, (x - r, y - r), special_flags=pygame.BLEND_RGBA_ADD)

            if in_active_zone:
                ball_alpha = int(255 * (1.0 - 0.65 * glow_factor))
            else:
                if note.y < self.pre_hit_end:
                    ball_alpha = min(255, int(80 + (note.y / self.pre_hit_end) * 175))
                else:
                    ball_alpha = 255

            ball_radius = max(1, int(self.note_radius * pulse))
            ball_surf = pygame.Surface((ball_radius * 2, ball_radius * 2), pygame.SRCALPHA)
            for i in range(ball_radius, 0, -3):
                t = i / ball_radius
                r_c = int(255 * (1 - t) + lane_color[0] * t)
                g_c = int(255 * (1 - t) + lane_color[1] * t)
                b_c = int(255 * (1 - t) + lane_color[2] * t)
                a = int(ball_alpha * (1.0 - t * 0.6))
                if a > 0:
                    pygame.draw.circle(ball_surf, (r_c, g_c, b_c, a), (ball_radius, ball_radius), i)
            surface.blit(ball_surf, (x - ball_radius, y - ball_radius))

            if in_active_zone and glow_factor > 0.2:
                ring_alpha = int(200 * glow_factor)
                ring_r = ball_radius + 4
                ring_surf = pygame.Surface((ring_r * 2, ring_r * 2), pygame.SRCALPHA)
                pygame.draw.circle(ring_surf, (255, 255, 255, ring_alpha),(ring_r, ring_r), ring_r, 2)
                surface.blit(ring_surf, (x - ring_r, y - ring_r),special_flags=pygame.BLEND_RGBA_ADD)

        def _spawn_hit_particles(self, x, y, lane):
            color = self.lane_colors[lane]
            base_count = 20
            bonus = min(40, self.combo * 2)
            total = base_count + bonus

            for _ in range(total):
                self.particles.append(Particle(x, y, color, size_range=(3, 8)))
            for _ in range(total // 2):
                self.particles.append(Particle(x, y, (255, 255, 255), size_range=(2, 4)))
            for _ in range(total // 3):
                self.particles.append(Particle(x, y, (255, 220, 100), size_range=(2, 5)))

            self.flashes.append(Flash(x, y, (255, 255, 255), max_radius=100))
            self.flashes.append(Flash(x, y, color, max_radius=70))

        def _update_and_draw_particles(self, surface, dt):
            self.particles = [p for p in self.particles if p.update(dt)]
            if self.particles:
                p_surf = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
                for p in self.particles:
                    p.draw(p_surf)
                surface.blit(p_surf, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)

        def _update_and_draw_flashes(self, surface, dt):
            self.flashes = [f for f in self.flashes if f.update(dt)]
            for f in self.flashes:
                f.draw(surface)

        # ИЗМЕНЕНО: отклик клавиши на ЛЮБОЕ нажатие, не только при попадании
        def event(self, ev, x, y, st):
            if not self.is_playing:
                return None
            if ev.type == pygame.QUIT:
                self.stop()
                renpy.music.stop()
                renpy.end_interaction(None)
                return None
            if ev.type == pygame.KEYDOWN:
                # НОВОЕ: ESC выходит из игры (keymap чистый, но event() всё равно получает события)
                if ev.key == pygame.K_ESCAPE:
                    self.stop()
                    renpy.music.stop()
                    renpy.end_interaction(None)
                    return None
                lane = -1
                if ev.key in self.key_map:
                    lane = self.key_map[ev.key]
                else:
                    unicode_char = getattr(ev, 'unicode', '')
                    if unicode_char:
                        lower_char = unicode_char.lower()
                        if lower_char in self.unicode_map:
                            lane = self.unicode_map[lower_char]

                if lane != -1:
                    # НОВОЕ: визуальный отклик на любое нажатие клавиши
                    self.lane_press_timer[lane] = self.PRESS_DURATION
                    self._check_hit(lane)

                return None

            return None

        def _check_hit(self, lane):
            stats = self.get_difficulty_stats()
            best_note = None
            best_dist = float('inf')
            for note in self.notes:
                if note.lane == lane and note.active and not note.is_hit and not note.has_missed:
                    if self.pre_hit_end <= note.y <= self.missed_start:
                        dist = abs(note.y - self.hit_center)
                        if dist < best_dist:
                            best_dist = dist
                            best_note = note

            if best_note is not None and best_dist <= stats["tolerance"]:
                best_note.is_hit = True
                best_note.hit_progress = 0.0
                self.score += stats["points"]
                self.combo += 1
                if self.combo > self.max_combo:
                    self.max_combo = self.combo
                renpy.store.char_dance_state = stats["state"]
                if self.combo in (self.COMBO_X10, self.COMBO_X20, self.COMBO_RASKOLBAS):
                    self.combo_milestone = self.combo
                    self.milestone_timer = 1.5
                renpy.restart_interaction()

        def start(self):
            self.is_playing = True
            self.game_time = 0.0
            self.current_note_index = 0
            self.last_st = None
            self.score = 0
            self.combo = 0
            self.max_combo = 0
            self.particles = []
            self.flashes = []
            self.combo_milestone = None
            self.milestone_timer = 0.0
            self.lane_press_timer = [0.0] * self.lanes  # НОВОЕ
            self._load_notes()
            renpy.store.char_dance_state = "normal"
            global stumble_timer
            stumble_timer = 0.0
            lock_renpy_keyboard()

        def stop(self):
            self.is_playing = False
            unlock_renpy_keyboard()

    def lane_hint_dance(trans, st, at, lane_idx):
        """ATL-функция: каждый кадр читает lane_press_timer[lane_idx] из rhythm_game
        и применяет yoffset (нажатие) и alpha (яркость)."""
        rg = getattr(renpy.store, 'rhythm_game', None)
        if rg is None or not rg.is_playing:
            trans.yoffset = 0
            trans.alpha = 0.3
            return 0
        if lane_idx >= len(rg.lane_press_timer):
            return 0
        timer_val = rg.lane_press_timer[lane_idx]
        press_duration = rg.PRESS_DURATION
        # press_intensity = 1.0 только что нажата, 0.0 в покое
        press_intensity = max(0.0, min(1.0, timer_val / press_duration))
        trans.yoffset = int(4 * press_intensity)
        # alpha от 0.3 (покой) до 1.0 (нажата)
        trans.alpha = 0.3 + 0.7 * press_intensity
        return 0  # 0 = вызывать каждый кадр
    def _hint_d(trans, st, at):
        return lane_hint_dance(trans, st, at, 0)
    def _hint_f(trans, st, at):
        return lane_hint_dance(trans, st, at, 1)
    def _hint_j(trans, st, at):
        return lane_hint_dance(trans, st, at, 2)
    def _hint_k(trans, st, at):
        return lane_hint_dance(trans, st, at, 3)
# === DISPLAYABLE: ТАНЦОР ===
# ConditionSwitch автоматически меняет анимацию при изменении char_dance_state
image dancer = ConditionSwitch(
    "char_dance_state == 'stumble'", dance_stumble_anim,
    "char_dance_state in ('raskolbas', 'ultra_raskolbas')", dance_raskolbas_anim,
    "True", dance_normal_anim
)

# === АНИМАЦИИ ===

transform combo_milestone_popup:
    zoom 0.0 alpha 0.0
    easeout 0.2 zoom 1.3 alpha 1.0
    linear 0.4 zoom 1.2 alpha 1.0
    easein 0.4 zoom 1.6 alpha 0.0
# НОВОЕ: трансформы для подсказок клавиш
transform lane_hint_d:
    function _hint_d
transform lane_hint_f:
    function _hint_f
transform lane_hint_j:
    function _hint_j
transform lane_hint_k:
    function _hint_k
transform fire_raskolbas_popup:
    parallel:
        matrixcolor TintMatrix("#ff0000")
        linear 0.05 matrixcolor TintMatrix("#ff7f00")
        linear 0.05 matrixcolor TintMatrix("#ffff00")
        linear 0.05 matrixcolor TintMatrix("#00ff00")
        linear 0.05 matrixcolor TintMatrix("#0000ff")
        linear 0.05 matrixcolor TintMatrix("#4b0082")
        linear 0.05 matrixcolor TintMatrix("#8b00ff")
        linear 0.05 matrixcolor TintMatrix("#ff0000")
    repeat
    parallel:
        zoom 0.0 alpha 0.0
        easeout 0.25 zoom 1.4 alpha 1.0
        linear 0.6 zoom 1.25 alpha 1.0
        easein 0.5 zoom 1.7 alpha 0.0

transform combo_float:
    yoffset 0
    linear 0.5 yoffset -5
    linear 0.5 yoffset 0
    repeat


screen rhythm_ui():
    zorder 100

    timer 0.05 repeat True action Function(renpy.restart_interaction)

    frame:
        background Solid("#000000aa")
        xalign 0.02
        yalign 0.02
        xpadding 25
        ypadding 12
        xminimum 280
        vbox:
            xalign 0.5
            text "SCORE" size 18 color "#888888" xalign 0.5
            text "[rhythm_game.score]" size 48 color "#ffffff" bold True xalign 0.5

    if rhythm_game.combo > 0:
        if rhythm_game.combo >= 15:
            $ combo_color = "#ff3333"
        elif rhythm_game.combo >= 10:
            $ combo_color = "#ff33ff"
        elif rhythm_game.combo >= 5:
            $ combo_color = "#ff8800"
        else:
            $ combo_color = "#ffc800"

        text "x[rhythm_game.combo]" size 50 color combo_color bold True xalign 0.98 yalign 0.02 at combo_float

    if rhythm_game.combo_milestone == 5:
        text "COMBO x5!" size 100 color "#ffc800" bold True xalign 0.5 yalign 0.3 at combo_milestone_popup
    elif rhythm_game.combo_milestone == 10:
        text "COMBO x10!" size 110 color "#ff33ff" bold True xalign 0.5 yalign 0.3 at combo_milestone_popup
    elif rhythm_game.combo_milestone == 15:
        text "РАСКОЛБАС!" size 130 color "#ffffff" bold True xalign 0.5 yalign 0.3 at fire_raskolbas_popup
    text "D" size 36 color "#ffffff" bold True xalign 0.125 yalign 0.95 at lane_hint_d
    text "F" size 36 color "#ffffff" bold True xalign 0.375 yalign 0.95 at lane_hint_f
    text "J" size 36 color "#ffffff" bold True xalign 0.625 yalign 0.95 at lane_hint_j
    text "K" size 36 color "#ffffff" bold True xalign 0.875 yalign 0.95 at lane_hint_k