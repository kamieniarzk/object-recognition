import sys


class BoundingBox:
    def __init__(self):
        self.is_valid = True
        self.y_min = sys.maxsize
        self.y_max = -1
        self.x_min = sys.maxsize
        self.x_max = -1
        self.pixel_coords = []
        self.border_pixels = []
        self.border_length = 0

    def add_pixel(self, y, x, is_edge):
        if y > self.y_max:
            self.y_max = y
        if y < self.y_min:
            self.y_min = y
        if x > self.x_max:
            self.x_max = x
        if x < self.x_min:
            self.x_min = x
        self.pixel_coords.append((y, x))
        if is_edge:
            self.border_length += 1
            self.border_pixels.append((y, x))

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

    def to_string(self):
        return 'is_valid: {}, row_min: {}, row_max: {}, col_min: {}, col_max: {}, border_length: {}'\
            .format(self.is_valid, self.y_min, self.y_max, self.x_min, self.x_max, self.border_length)
