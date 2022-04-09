import re
import numpy as np


class PatternDrawer:
    def __init__(self, pattern_str, shape_wh, unit_size, first_hole_angle_deg=0, holes_num=4, hole_diameter=4):
        self.shape_wh = shape_wh
        self.unit_size = unit_size
        self.first_hole_angle_deg = first_hole_angle_deg
        self.holes_num = holes_num
        self.hole_diameter = hole_diameter

        self.pattern_mask = self._parse_pattern_str(pattern_str)

    def _parse_pattern_str(self, pattern_str):
        pattern_str = pattern_str.strip()

        mask = np.zeros(self.shape_wh, dtype=bool)

        res = re.fullmatch('[o.]+', pattern_str)
        if res is not None:
            w, h = self.shape_wh
            size = w * h

            pattern_len = len(res)
            if pattern_len != size:
                print(f'Wrong pattern string length! Expected {w}*{h}={size} symbols, found {pattern_len}')
                return None

            for i in range(w):
                for j in range(h):
                    idx = i + j * w
                    char = pattern_str[idx]
                    mask = [i, j] = char == 'o'

        comma_separated_numbers = '[0-9]+(,[0-9]+)*'
        regex = f'x:{comma_separated_numbers}\s+y:{comma_separated_numbers}'
        res = re.fullmatch(regex, pattern_str)
        if res is not None:
            x, y = pattern_str.split()

            x_steps = x[2:].split(',')
            x_steps = [int(s) for s in x_steps]

            y_steps = y[2:].split(',')
            y_steps = [int(s) for s in y_steps]

            def make_valid_line(length, steps):
                valid_line = np.zeros(length, dtype=bool)
                step_idx = 0
                idx = 0
                while idx < len(valid_line):
                    valid_line[idx] = True
                    idx += steps[step_idx]
                    step_idx = (step_idx + 1) % len(steps)

                return valid_line

            w, h = self.shape_wh
            valid_x = make_valid_line(
                length=w,
                steps=x_steps
            )
            valid_y = make_valid_line(
                length=h,
                steps=y_steps
            )

            mask[:] = True
            mask[~valid_x, :] = False
            mask[:, ~valid_y] = False

        return mask

    def _draw_circle_group(self, drawing, x_mm, y_mm):
        angles = np.deg2rad(self.first_hole_angle_deg) + \
                 np.linspace(0, 2 * np.pi, self.holes_num, endpoint=False)

        us = self.unit_size
        for angle in angles:
            x = (us / 2) + np.cos(angle) * (us / 4)
            y = (us / 2) - np.sin(angle) * (us / 4)

            drawing.circle(
                (x_mm + x, y_mm + y),
                self.hole_diameter,
                color='red',
            )

    def draw(self, drawing):
        w, h = self.shape_wh
        us = self.unit_size

        for i in range(w):
            for j in range(h):
                if self.pattern_mask[i, j]:
                    self._draw_circle_group(
                        drawing,
                        x_mm=us * i,
                        y_mm=us * j,
                    )
