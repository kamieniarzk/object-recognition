import numpy as np
from BoundingBox import BoundingBox
from typing import List

LINE_COLOR = [0, 0, 255]
X = 0
Y = 1


def draw_bounding_boxes(image: np.ndarray, bounding_boxes: List[BoundingBox]):
    for bounding_box in bounding_boxes:
        draw_bounding_box(image, bounding_box)


def draw_bounding_box(image: np.ndarray, box: BoundingBox):
    bottom_left = (box.y_max, box.x_min)
    bottom_right = (box.y_max, box.x_max)
    upper_left = (box.y_min, box.x_min)
    upper_right = (box.y_min, box.x_max)
    draw_line(image, bottom_left, upper_left)
    draw_line(image, bottom_left, bottom_right)
    draw_line(image, upper_left, upper_right)
    draw_line(image, upper_right, bottom_right)


def draw_line(image: np.ndarray, point1: [], point2: []):
    start = point1
    end = point2
    if start[X] > end[X]:
        start = point2
        end = point1
    elif start[X] == end[X]:
        if start[Y] > end[Y]:
            start = point2
            end = point1
    for i in range(start[X], end[X] + 1):
        for j in range(start[Y], end[Y] + 1):
            image[i, j] = LINE_COLOR
