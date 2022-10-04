import copy
import json
import scipy.signal
import numpy as np
from typing import Tuple, NamedTuple
from dataclasses import dataclass
from collections.abc import Sequence, MutableSequence

from drawings.dxf_drawing import DxfDrawing


@dataclass
class Part:
    name: str
    path_no_ext: str
    shape_wh: Tuple[int, int]
    number: int


class PartsPlacer:
    class PlacingCandidate(NamedTuple):
        name: str
        part_idx: int
        orientation_idx: int
        sheet_idx: int
        pos_xy: Tuple[int, int]
        score: float

    class PlacedPart(NamedTuple):
        part: Part
        angle_deg: int
        pos_xy: Tuple[int, int]

    def __init__(
            self,
            parts: Sequence[Part],
            work_area_wh: [int, int],
            unit_size: float = 1.0,
            h_to_v_coef_ratio: float = 20.0
    ):
        for part in parts:
            assert part.number > 0, f'Incorrect number of parts for part "{part.name}": it should be >= 0'

        self.parts = parts
        self.work_area_wh = work_area_wh
        self.unit_size = unit_size
        self.h_to_v_coef_ratio = h_to_v_coef_ratio

        parts_by_name = {}
        for part in parts:
            name = part.name
            assert name not in parts_by_name, 'Error: duplicate part names!'
            parts_by_name[name] = part
        self.parts_by_name = parts_by_name

        self.placed_parts = None
        self.sheets_number = 0

        self.dxf_drawing = DxfDrawing()

    def _initialize_score_map(self, sheet_idx):
        ww, hh = self.work_area_wh
        v_coef = 1.0
        h_coef = v_coef * self.h_to_v_coef_ratio

        # h-score
        h_score_max = ww * h_coef
        h_score_1d = np.linspace(
            h_score_max,
            h_score_max / 2,
            ww
        )
        h_score = np.repeat(
            np.expand_dims(h_score_1d, axis=0),
            hh,
            axis=0
        )

        # v-score
        v_score_max = ww * v_coef
        v_score_1d = np.linspace(
            v_score_max,
            0,
            hh,
        )
        v_score = np.repeat(
            np.expand_dims(v_score_1d, axis=1),
            ww,
            axis=1
        )

        # total score
        score_map = h_score + v_score

        score_map /= 2.5**sheet_idx

        return score_map

    def place(self):
        ww, hh = self.work_area_wh

        score_maps_by_sheet = [
            self._initialize_score_map(sheet_idx=0)
        ]
        parts_queue: MutableSequence[Part] = list(copy.deepcopy(self.parts))
        placed_parts = []
        while True:
            if len(parts_queue) == 0:
                break

            placing_candidates = []
            for part_idx, part in enumerate(parts_queue):
                pw, ph = part.shape_wh

                is_orient_ok = [
                    pw <= ww and ph <= hh,
                    pw <= hh and ph <= ww,
                ]
                if np.sum(is_orient_ok) == 0:
                    raise Exception(
                        f'Part {part.name} does not fit in work area: {part.shape_wh} > {self.work_area_wh}'
                    )

                orientations = []
                for i in range(len(is_orient_ok)):
                    if not is_orient_ok[i]:
                        continue

                    part_wh = [[pw, ph], [ph, pw]][i]
                    orientations.append({
                        'orientation_idx': i,
                        'part_wh': part_wh,
                    })

                for orientation in orientations:
                    orientation_idx = orientation['orientation_idx']
                    w, h = orientation['part_wh']

                    sheet_idx = 0
                    while sheet_idx < len(score_maps_by_sheet):
                        score_map = score_maps_by_sheet[sheet_idx]

                        kernel = np.ones((h, w), dtype=float)
                        scores = scipy.signal.convolve2d(score_map, kernel, 'valid')

                        best_score = np.max(scores)

                        sh, sw = scores.shape
                        best_pos_1d = np.argmax(scores)
                        best_pos_xy = (
                            best_pos_1d % sw,
                            best_pos_1d // sw,
                        )

                        if best_score == -np.inf:
                            sheets_num = len(score_maps_by_sheet)
                            is_last_sheet = sheet_idx == (sheets_num - 1)
                            if is_last_sheet:
                                score_maps_by_sheet.append(
                                    self._initialize_score_map(sheet_idx=sheets_num)
                                )
                        else:
                            candidate = self.PlacingCandidate(
                                name=part.name,
                                part_idx=part_idx,
                                orientation_idx=orientation_idx,
                                sheet_idx=sheet_idx,
                                pos_xy=best_pos_xy,
                                score=best_score,
                            )
                            placing_candidates.append(candidate)

                        sheet_idx += 1

            best_candidate = max(placing_candidates, key=lambda x: x.score)

            # ~~~~~~~~update everything~~~~~~~~~~
            x, y = best_candidate.pos_xy
            w, h = self.parts_by_name[best_candidate.name].shape_wh
            if best_candidate.orientation_idx == 1:
                w, h = h, w
            score_map = score_maps_by_sheet[best_candidate.sheet_idx]
            score_map[y:y + h, x:x + w] = -np.inf

            part_idx = best_candidate.part_idx
            part = parts_queue[part_idx]
            part.number -= 1
            if part.number == 0:
                del parts_queue[part_idx]

            print('Placing', part.name)
            # ~~~~~debug~~~~~~~
            # import matplotlib.pyplot as plt
            # h, w = score_maps_by_sheet[0].shape
            # img = np.zeros((h, w * 6))
            # for i in range(len(score_maps_by_sheet)):
            #     img[:, i * w:(i + 1) * w] = score_maps_by_sheet[i]
            # plt.imshow(img)
            # plt.colorbar()
            # plt.show()
            # ~~~~~~~~

            angle_deg = [0, -90][best_candidate.orientation_idx]
            w, h = part.shape_wh
            x, y = best_candidate.pos_xy
            dy = [0, w][best_candidate.orientation_idx]
            sheet_dx = ww * 1.5 * best_candidate.sheet_idx
            pos_xy = (x + sheet_dx, y + dy)
            placed_part = self.PlacedPart(
                part=part,
                angle_deg=angle_deg,
                pos_xy=pos_xy
            )
            placed_parts.append(placed_part)

        self.placed_parts = placed_parts
        self.sheets_number = len(score_maps_by_sheet)

    def draw(self):
        for part in self.placed_parts:
            translate_xy = np.array(part.pos_xy) * self.unit_size

            self.dxf_drawing.subdrawing(
                subdrawing_file=part.part.path_no_ext,
                translate_xy=translate_xy,
                rotate_deg=part.angle_deg,
                is_no_ext=True
            )

    def write(self, file_no_ext):
        self.dxf_drawing.write(file_no_ext, is_no_ext=True)

        total_length_mm = self.dxf_drawing.get_total_lines_length_mm()
        total_length_m = total_length_mm / 1000
        total_length_m = round(total_length_m, 3)
        data = {
            'work_area_wh': self.work_area_wh,
            'unit_size': self.unit_size,
            'sheets_number': self.sheets_number,
            'total_length_m':  total_length_m
        }
        print(data)
        with open(f'{file_no_ext}.json', 'w') as outf:
            json.dump(
                data,
                outf,
                indent=4,
            )


