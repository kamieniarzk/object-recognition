import numpy as np

from BoundingBox import BoundingBox
from numba import jit

WHITE_PIXEL = 255
ALREADY_SEEN = 1
UNSEEN = 0


class BoundingBoxesExtractor:
    def __init__(self, image: np.ndarray):
        h, w = image.shape
        self.height = h
        self.width = w
        self.seen_pixels_cache = np.full((self.height, self.width), UNSEEN, dtype=np.uint8)
        self.image = image
        self.boxes = []

    def get_bounding_boxes(self):
        for i in range(1, self.height - 1):
            for j in range(1, self.width - 1):
                if self.seen_pixels_cache[i, j] != ALREADY_SEEN and self.image[i, j] == WHITE_PIXEL:
                    self.entry_point(i, j)

        return self.boxes

    def entry_point(self, y: int, x: int):
        pixels_to_see = [(y, x)]
        bounding_box = BoundingBox()
        while pixels_to_see:
            row, col = pixels_to_see.pop()
            if self.see_pixel(row, col, bounding_box):
                pixels_to_see.extend(self.get_connected_neighbours_indexes(row, col))
        self.boxes.append(bounding_box)

    def see_pixel(self, y: int, x: int, box: BoundingBox):
        self.seen_pixels_cache[y, x] = ALREADY_SEEN
        if self.image[y, x] != WHITE_PIXEL:
            return False

        box.push_pixel(y, x)
        return True

    def get_connected_neighbours_indexes(self, y: int, x: int):
        if self.is_at_image_border(self.height, self.width, y, x):
            return []

        connected_neighbours_indexes = []
        neighbour_indexes = [(i, j) for i in range(y - 1, y + 2) for j in range(x - 1, x + 2)]
        for neighbour_index in neighbour_indexes:
            if self.seen_pixels_cache[neighbour_index] == UNSEEN and self.image[neighbour_index] == WHITE_PIXEL:
                connected_neighbours_indexes.append(neighbour_index)

        return connected_neighbours_indexes

    @staticmethod
    @jit
    def is_at_image_border(height: int, width: int, y: int, x: int):
        return x <= 0 or x >= width - 1 or y <= 0 or y >= height - 1