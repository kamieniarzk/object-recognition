import numpy as np
from BoundingBox import BoundingBox
from typing import List


X = 0
Y = 1


def draw_bounding_boxes(image: np.ndarray, bounding_boxes: List[BoundingBox]):
    for bounding_box in bounding_boxes:
        draw_bounding_box(image, bounding_box)


def draw_bounding_box(image, box):
    bottom_left = (box.y_max, box.x_min)
    bottom_right = (box.y_max, box.x_max)
    upper_left = (box.y_min, box.x_min)
    upper_right = (box.y_min, box.x_max)
    draw_line(image, bottom_left, upper_left)
    draw_line(image, bottom_left, bottom_right)
    draw_line(image, upper_left, upper_right)
    draw_line(image, upper_right, bottom_right)


def draw_line(image, point1, point2):
    start_point = point1
    end_point = point2
    if start_point[X] > end_point[X]:
        start_point = point2
        end_point = point1
    elif start_point[X] == end_point[X]:
        if start_point[Y] > end_point[Y]:
            start_point = point2
            end_point = point1
    for i in range(start_point[X], end_point[X] + 1):
        for j in range(start_point[Y], end_point[Y] + 1):
            image[i, j] = [0, 0, 255]