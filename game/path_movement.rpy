init python:
    class PathInterpolator(object):

        anchors = {
            'top': 0.0,
            'center': 0.5,
            'bottom': 1.0,
            'left': 0.0,
            'right': 1.0,
        }

        # Default anchors (from Position)
        default_anchors = (1, 1)

        def __init__(self, points):
            assert len(points) >= 2, "Need at least a start and end point."

            def setup_coordinate_(c):
                if len(c) == 2:
                    c += self.default_anchors
                return [self.anchors.get(i, i) for i in c]

            self.points = []

            for p in points:
                length = len(p)

                if isinstance(p[-1], float):
                    length = len(p) - 1
                    point = [p[-1]]
                else:
                    length = len(p)
                    point = [-1]

                self.points.append(point + [setup_coordinate_(p) for i in range(length)])

            # Make sure start and end times are set, if not already set
            if self.points[0][0] == -1:
                self.points[0][0] = 0.0
            if self.points[-1][0] == -1:
                self.points[-1][0] = 1.0

            # Now we gotta calculate the step times that need calculating
            for start in range(1, len(self.points) - 1):
                if self.points[start][0] != -1:
                    continue

                end = start + 1

                while end < (len(self.points) - 1) and self.points[end][0] == -1:
                    end += 1

                step = (self.points[end][0] - self.points[start - 1][0]) / float(end - start + 1)

                for i in range(start, end):
                    self.points[i][0] = self.points[i - 1][0] + step

            # And finally, sort the list of points by increasing time
            self.points.sort(key=lambda a: a[0])

            self.initialized = False

        def init_values_(self, sizes):
            def to_abs_(value, size):
                if isinstance(value, float):
                    return value * size
                else:
                    return value

            def coord_(c):
                # Проверяем, является ли элемент кортежем
                if isinstance(c[0], tuple):
                    x, y = c[0]  # Распаковываем координаты из кортежа
                else:
                    x, y = c[0], c[1]

                # Обрабатываем привязки (anchor points), если они есть
                anchor_x = to_abs_(c[2], sizes[2]) if len(c) > 2 else 0
                anchor_y = to_abs_(c[3], sizes[3]) if len(c) > 3 else 0

                # Возвращаем окончательную координату
                return [to_abs_(x, sizes[0]) - anchor_x, to_abs_(y, sizes[1]) - anchor_y]


            for p in self.points:
                for i in range(1, len(p)):
                    p[i] = coord_(p[i])

            self.initialized = True

        def __call__(self, t, sizes):
            # Initialize if necessary
            if not self.initialized:
                self.init_values_(sizes)

            # Now we must determine which segment we are in
            for segment in range(len(self.points)):
                if self.points[segment][0] > t:
                    break

            # If this is the zeroth segment, just start at the start point
            if segment == 0:
                result = self.points[0][1]
            # If this is past the last segment, just leave it at the end point
            elif segment == len(self.points) - 1 and t > self.points[-1][0]:
                result = self.points[-1][1]
            else:
                # Scale t
                t = (t - self.points[segment - 1][0]) / (self.points[segment][0] - self.points[segment - 1][0])

                # Get start and end points
                start = self.points[segment - 1][1]
                end = self.points[segment][1]

                # Now what kind of interpolation is it?
                if len(self.points[segment]) == 2:  # Straight line
                    t_p = 1.0 - t
                    result = [t_p * start[i] + t * end[i] for i in (0, 1)]
                elif len(self.points[segment]) == 3:  # Quadratic Bézier
                    t_pp = (1.0 - t)**2
                    t_p = 2 * t * (1.0 - t)
                    t2 = t**2
                    result = [
                        t_pp * start[i] + t_p * self.points[segment][2][i] + t2 * end[i] for i in (0, 1)
                    ]
                elif len(self.points[segment]) == 4:  # Cubic Bézier
                    t_ppp = (1.0 - t)**3
                    t_pp = 3 * t * (1.0 - t)**2
                    t_p = 3 * t**2 * (1.0 - t)
                    t3 = t**3
                    result = [
                        t_ppp * start[i]
                        + t_pp * self.points[segment][2][i]
                        + t_p * self.points[segment][3][i]
                        + t3 * end[i]
                        for i in (0, 1)
                    ]

            return (int(result[0]), int(result[1]), 0, 0)

    def PathMotion(points, time, child=None, repeat=False, bounce=False, anim_timebase=False, style='default', time_warp=None, **properties):
        return Motion(
            PathInterpolator(points),
            time,
            child,
            repeat=repeat,
            bounce=bounce,
            anim_timebase=anim_timebase,
            style=style,
            time_warp=time_warp,
            add_sizes=True,
            **properties
        )

    def clamp(value, min_value, max_value):
        """Ограничивает значение в пределах min_value и max_value"""
        return max(min_value, min(value, max_value))

    def calculate_trajectory(start, end, object_size=(800, 300), screen_size=(1920, 1080)):
        trajectory = []
        
        x, y = start  # стартовая позиция
        x_end, y_end = end  # конечная позиция
        dx, dy = 5, 5  # скорость движения объекта по X и Y (выстави свои значения)
        o_x, o_y = object_size  # размер объекта по X и Y
        
        max_x, max_y = screen_size  # максимальные координаты
        min_x = 300  # минимальные координаты по X (ограничения для панели)
        min_y = 0  # минимальные координаты по Y (верхний край)
        
        trajectory.append((x, y))  # добавляем стартовую точку сразу
        
        direction_x = 1  # начальное направление по X
        direction_y = 1  # начальное направление по Y
        
        # Цикл для кругового движения
        while True:
            # Двигаемся по диагонали (одновременно по X и Y)
            x += dx * direction_x
            y += dy * direction_y
            
            # Столкновения с границами и изменение направления
            if x <= min_x:  # столкновение с левой границей
                x = min_x
                direction_x = 1  # меняем направление по X (вправо)
            elif x >= max_x - o_x:  # столкновение с правой границей
                x = max_x - o_x
                direction_x = -1  # меняем направление по X (влево)

            if y <= min_y:  # столкновение с верхней границей
                y = min_y
                direction_y = 1  # меняем направление по Y (вниз)
            elif y >= max_y - o_y:  # столкновение с нижней границей
                y = max_y - o_y
                direction_y = -1  # меняем направление по Y (вверх)

            # Ограничиваем координаты объекта в пределах экрана с использованием clamp
            x = clamp(x, min_x, max_x - o_x)
            y = clamp(y, min_y, max_y - o_y)

            trajectory.append((x, y))  # добавляем текущую позицию

            # Проверка, если вернулись в начальную точку
            if (x, y) == start:
                break  # выход из цикла, когда вернулись в начальную точку

        return trajectory

define adjusted_bounce_path=calculate_trajectory((300,0),(300,0))

