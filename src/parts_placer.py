import copy
import scipy.signal
import numpy as np
from typing import Tuple, NamedTuple
from dataclasses import dataclass
from collections.abc import Sequence, MutableSequence

from src.drawings.dxf_drawing import DxfDrawing


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
        pos_xy: Tuple[int, int]
        score: float

    class PlacedPart(NamedTuple):
        part: Part
        angle_deg: int
        pos_xy: Tuple[int, int]

    def __init__(self, parts: Sequence[Part], work_area_wh: [int, int], unit_size: float = 1.0):
        for part in parts:
            assert part.number > 0, f'Incorrect number of parts for part "{part.name}": it should be >= 0'

        self.parts = parts
        self.work_area_wh = work_area_wh
        self.unit_size = unit_size

        parts_by_name = {}
        for part in parts:
            name = part.name
            assert name not in parts_by_name, 'Error: duplicate part names!'
            parts_by_name[name] = part
        self.parts_by_name = parts_by_name

        self.dxf_drawing = DxfDrawing()

    def _initialize_score_map(self):
        ww, hh = self.work_area_wh

        # h-score
        h_score_1d = np.linspace(500, 0, ww)
        h_score = np.repeat(
            np.expand_dims(h_score_1d, axis=0),
            hh,
            axis=0
        )

        # v-score
        v_score_1d = np.linspace(100, 0, hh)
        v_score = np.repeat(
            np.expand_dims(v_score_1d, axis=1),
            ww,
            axis=1
        )

        # total score
        score_map = h_score + v_score
        return score_map

    def place(self) -> Sequence[PlacedPart]:
        score_map = self._initialize_score_map()
        parts_queue: MutableSequence[Part] = list(copy.deepcopy(self.parts))
        placed_parts = []
        while True:
            if len(parts_queue) == 0:
                break

            placing_candidates = []
            for part_idx, part in enumerate(parts_queue):
                pw, ph = part.shape_wh
                orientations = [[pw, ph], [ph, pw]]
                for orientation_idx, part_wh in enumerate(orientations):
                    w, h = orientations[orientation_idx]

                    kernel = np.ones((h, w), dtype=float)
                    scores = scipy.signal.convolve2d(score_map, kernel, 'valid')

                    best_score = np.max(scores)

                    sh, sw = scores.shape
                    best_pos_1d = np.argmax(scores)
                    best_pos_xy = (
                        best_pos_1d % sw,
                        best_pos_1d // sw,
                    )

                    candidate = self.PlacingCandidate(
                        name=part.name,
                        part_idx=part_idx,
                        orientation_idx=orientation_idx,
                        pos_xy=best_pos_xy,
                        score=best_score,
                    )
                    placing_candidates.append(candidate)

            best_candidate = max(placing_candidates, key=lambda x: x.score)

            if best_candidate.score == -np.inf:
                print('Failed to place all parts in one sheet!')
                break

            # ~~~~~~~~update everything~~~~~~~~~~
            x, y = best_candidate.pos_xy
            w, h = self.parts_by_name[best_candidate.name].shape_wh
            if best_candidate.orientation_idx == 1:
                w, h = h, w
            score_map[y:y + h, x:x + w] = -np.inf

            # import matplotlib.pyplot as plt
            # plt.imshow(score_map)
            # plt.colorbar()
            # plt.show()

            part_idx = best_candidate.part_idx
            part = parts_queue[part_idx]
            part.number -= 1
            if part.number == 0:
                del parts_queue[part_idx]

            angle_deg = [0, -90][best_candidate.orientation_idx]
            w, h = part.shape_wh
            x, y = best_candidate.pos_xy
            dy = [0, w][best_candidate.orientation_idx]
            pos_xy = (x, y + dy)
            placed_part = self.PlacedPart(
                part=part,
                angle_deg=angle_deg,
                pos_xy=pos_xy
            )
            placed_parts.append(placed_part)

        return placed_parts

    def draw(self, placed_parts):
        for part in placed_parts:
            translate_xy = np.array(part.pos_xy) * self.unit_size

            self.dxf_drawing.subdrawing(
                subdrawing_file=part.part.path_no_ext,
                translate_xy=translate_xy,
                rotate_deg=part.angle_deg,
                is_no_ext=True
            )

    def write(self, file):
        self.dxf_drawing.write(file)
