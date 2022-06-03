import sys
import numpy as np


class Box:
    def __init__(self, box_color):
        self.is_valid = True
        self.box_color = box_color
        self.row_min = sys.maxsize
        self.row_max = -1
        self.col_min = sys.maxsize
        self.col_max = -1
        self.pixel_coords = []
        self.border_pixels = []
        self.border_length = 0

    def add_point(self, row, col, is_border):
        if row > self.row_max:
            self.row_max = row
        if row < self.row_min:
            self.row_min = row
        if col > self.col_max:
            self.col_max = col
        if col < self.col_min:
            self.col_min = col
        self.pixel_coords.append((row, col))
        if is_border:
            self.border_length += 1
            self.border_pixels.append((row, col))

    def contains(self, box):
        return box.row_min > self.row_min and box.row_max < self.row_max \
               and box.col_min > self.col_min and box.col_max < self.col_max

    def get_width(self):
        return self.col_max - self.col_min

    def get_height(self):
        return self.row_max - self.row_min

    def get_box_area(self):
        return self.get_width() * self.get_height()

    def distance(self, box):
        vertical_dist = self.__get_vertical_dist(box)
        horizontal_dist = self.__get_horizonta_dist(box)
        return np.sqrt(vertical_dist ** 2 + horizontal_dist ** 2)

    def __get_vertical_dist(self, box):
        if box.row_min > self.row_max:
            return box.row_min - self.row_max
        elif box.row_max < self.row_min:
            return self.row_min - box.row_max
        else:
            return 0

    def __get_horizonta_dist(self, box):
        if box.col_max < self.col_min:
            return self.col_min - box.col_max
        elif box.col_min > self.col_max:
            return box.col_min - self.col_max
        else:
            return 0

    def is_clusterable(self):
        return not (self.col_min < 0 or self.row_min < 0 or
                    self.col_max > 100000 or self.row_max > 100000 or
                    self.get_height() < 5 or self.get_width() < 5)

    def combine(self, box):
        combined = Box(self.box_color)
        combined.col_max = np.maximum(self.col_max, box.col_max)
        combined.col_min = np.minimum(self.col_min, box.col_min)
        combined.row_max = np.maximum(self.row_max, box.row_max)
        combined.row_min = np.minimum(self.row_min, box.row_min)
        return combined

    def set_col_max(self, ncol_max):
        self.col_max = int(ncol_max)
        self.is_valid = False

    def set_col_min(self, ncol_min):
        self.col_min = int(ncol_min)
        self.is_valid = False

    def set_row_max(self, nrow_max):
        self.row_max = int(nrow_max)
        self.is_valid = False

    def set_row_min(self, nrow_min):
        self.row_min = int(nrow_min)
        self.is_valid = False

    def to_string(self):
        return 'is_valid: {}, box_color: {}, row_min: {}, row_max: {}, col_min: {}, col_max: {}, border_pixels: {}, border_length: {}'\
            .format(self.is_valid, self.box_color, self.row_min, self.row_max, self.col_min, self.col_max, self.border_pixels, self.border_length)
        # self.is_valid = True
        # self.box_color = box_color
        # self.row_min = sys.maxsize
        # self.row_max = -1
        # self.col_min = sys.maxsize
        # self.col_max = -1
        # self.pixel_coords = []
        # self.border_pixels = []
        # self.border_length = 0