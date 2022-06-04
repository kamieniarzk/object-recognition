import numpy as np
from BoundingBox import BoundingBox

WHITE_PIXEL = 255
ALREADY_SEEN = 1
UNSEEN = -1


class BoundingBoxesExtractor:
    def __init__(self, image: np.ndarray, rows, cols):
        self.height = rows
        self.width = cols
        self.seen_pixels_cache = np.full((rows, cols), -1)
        self.image = image
        self.boxes = []

    def get_bounding_boxes(self):
        for i in range(1, self.height - 1):
            for j in range(1, self.width - 1):
                if self.seen_pixels_cache[i, j] != ALREADY_SEEN and self.image[i, j] == WHITE_PIXEL:
                    self.entry_point(i, j)

        return self.boxes

    def entry_point(self, row, col):
        pixels_to_see = [(row, col)]
        bounding_box = BoundingBox()
        while pixels_to_see:
            row, col = pixels_to_see.pop()
            if self.see_pixel(row, col, bounding_box):
                pixels_to_see.extend(self.get_connected_neighbours_indexes(row, col))
        self.boxes.append(bounding_box)

    def see_pixel(self, row, col, box):
        if self.image[row, col] != WHITE_PIXEL:
            self.seen_pixels_cache[row, col] = UNSEEN
            return False

        box.add_pixel(row, col, self.is_edge(row, col))
        self.seen_pixels_cache[row, col] = ALREADY_SEEN
        return True

    def get_connected_neighbours_indexes(self, row, col):
        connected_neighbours_indexes = []
        if row == 0 or col == 0 or row == self.height - 1 or col == self.width - 1:
            return connected_neighbours_indexes

        neighbour_indexes = [(i, j) for i in range(row - 1, row + 2) for j in range(col - 1, col + 2)]
        for neighbour_index in neighbour_indexes:
            if self.seen_pixels_cache[neighbour_index] == UNSEEN and self.image[neighbour_index] == WHITE_PIXEL:
                connected_neighbours_indexes.append(neighbour_index)

        return connected_neighbours_indexes

    def is_edge(self, row, col):
        if row == 0 or col == 0 or row == self.height - 1 or col == self.width - 1:
            return False

        neighbour_pixels = [(i, j) for i in range(row - 1, row + 2) for j in range(col - 1, col + 2)]
        for neighbour_pixel in neighbour_pixels:
            if self.image[neighbour_pixel] != WHITE_PIXEL:
                return True

        return False
