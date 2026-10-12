init python:
    class LoveVariable:
        def __init__(self, name, lover="lars"):
            self._x = 0.0
            self.name = name
            self.lover = lover
            self.prev = 0.0
            
        @property
        def x(self):
            return self._x

        @x.setter
        def x(self, value):
            self._x = value
            renpy.show_screen("lovemeter", self)
            

        def __iadd__(self, value):
            self.x += value
            return self

        def __isub__(self, value):
            self.x -= value
            return self

        def __lt__(self, other):
            return self.x < other

        def __le__(self, other):
            return self.x <= other

        def __gt__(self, other):
            return self.x > other

        def __ge__(self, other):
            return self.x >= other

        def __eq__(self, other):
            return self.x == other

        def __ne__(self, other):
            return self.x != other

image scale = "gui/lovemeter values.png"
image arrow = "gui/lovemeter indicator.png"

init python:
    def calculate_rot(lover):
        start = 90
        step = 5
        return 90+lover*step

    def set_prev(lover):
        lover.prev = lover.x
        

transform rot(lover, prev):
    rotate calculate_rot(prev)
    linear 0.7 rotate calculate_rot(lover)



screen lovemeter(lover):
    window at notify_appear:
        style "lovebar"
        add "scale" xalign 0.25 yalign 0.2
        add "arrow" xalign 0.27 yalign 0.35 at rot(lover.x, lover.prev)
        hbox:
            xalign 0.25
            yalign 0.48
            add Image("gui/rel_"+lover.lover+".png") 
            text "{size=85}{color=#fff}+" yalign 0.7
            add Image("gui/rel_"+lover.name+".png") 
    timer 3.5 action [Hide("lovemeter"), Function(set_prev, lover)]

style lovebar:
    xalign 0.75
    yalign 0.3
