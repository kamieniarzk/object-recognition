def draw_boxes(image, boxes):
    for box in boxes:
        image = draw_box(image, box)
    return image


def draw_box(image, box):
    left_upper = (box.row_min, box.col_min)
    right_upper = (box.row_min, box.col_max)
    left_bottom = (box.row_max, box.col_min)
    right_bottom = (box.row_max, box.col_max)
    image = draw_line(image, left_bottom, left_upper)
    image = draw_line(image, left_bottom, right_bottom)
    image = draw_line(image, left_upper, right_upper)
    image = draw_line(image, right_upper, right_bottom)
    return image


def draw_line(image, point1, point2):
    start_point = point1
    end_point = point2
    if start_point[0] > end_point[0]:
        start_point = point2
        end_point = point1
    elif start_point[0] == end_point[0]:
        if start_point[1] > end_point[1]:
            start_point = point2
            end_point = point1
    for i in range(start_point[0], end_point[0] + 1):
        for j in range(start_point[1], end_point[1] + 1):
            image[i, j] = [0, 255, 0]
    return image
