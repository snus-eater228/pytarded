transform move_x(x, speed=0.5):
    yalign 1.0
    linear speed xalign x

transform move_x_from(f, x, speed=0.5):
    yalign 1.0
    xalign f
    linear speed xalign x
    
init python:
    def _get_lighting_transform():
        """Получает текущий трансформ освещения"""
        return getattr(renpy.store, f"lit_{store.current_light.value}", None)

    def move(tag, target_x, duration=0.5):
        # Собираем at_list с сохранением предыдущей позиции и добавлением света
        flat_at_list = list(_character_base_at_list.get(tag, []))
        flat_at_list.append(move_x(target_x, speed=duration))
        
        lighting = _get_lighting_transform()
        if lighting:
            flat_at_list.append(lighting)
        
        renpy.show(tag, at_list=flat_at_list)
        renpy.pause(duration, hard=False)
        
        # Фиксация конечной точки (тоже со светом!)
        flat_at_list_final = list(_character_base_at_list.get(tag, []))
        flat_at_list_final.append(Transform(yalign=1.0, xalign=target_x))
        if lighting:
            flat_at_list_final.append(lighting)
        
        renpy.show(tag, at_list=flat_at_list_final)

    def move_from(tag, start_x, target_x, duration=0.5):
        flat_at_list = list(_character_base_at_list.get(tag, []))
        flat_at_list.append(move_x_from(start_x, target_x, speed=duration))
        
        lighting = _get_lighting_transform()
        if lighting:
            flat_at_list.append(lighting)
        
        renpy.show(tag, at_list=flat_at_list)
        renpy.pause(duration, hard=False)
        
        # Фиксация
        flat_at_list_final = list(_character_base_at_list.get(tag, []))
        flat_at_list_final.append(Transform(yalign=1.0, xalign=target_x))
        if lighting:
            flat_at_list_final.append(lighting)
        
        renpy.show(tag, at_list=flat_at_list_final)
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
    
