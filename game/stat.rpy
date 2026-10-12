init python:
    class Stat:
        def __init__(self, name):
            self._x = 0.0
            self.name = name
            
        @property
        def x(self):
            return self._x

        @x.setter
        def x(self, value):
            self._x = value
            renpy.show_screen("stat", self.name)
           

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