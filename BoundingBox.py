import sys
import numpy as np


class BoundingBox:
    def __init__(self):
        self.x_min = sys.maxsize
        self.x_max = -1
        self.y_min = sys.maxsize
        self.y_max = -1

    def push_pixel(self, y: int, x: int):
        if y > self.y_max:
            self.y_max = y
        if y < self.y_min:
            self.y_min = y
        if x > self.x_max:
            self.x_max = x
        if x < self.x_min:
            self.x_min = x

    def get_width(self):
        return self.x_max - self.x_min

    def get_height(self):
        return self.y_max - self.y_min

    def get_box_area(self):
        return self.get_width() * self.get_height()

    def get_aspect_ratio(self):
        if self.get_height() != 0:
            return self.get_width() / self.get_height()
        return 0

    def get_from_image(self, img: np.ndarray):
        return img[self.y_min:self.y_max, self.x_min:self.x_max]

    def to_string(self):
        return 'row_min: {}, row_max: {}, col_min: {}, col_max: {}'\
            .format(self.y_min, self.y_max, self.x_min, self.x_max)
