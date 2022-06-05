from typing import List
import cv2
import numpy as np
from BoundingBoxesExtractor import BoundingBoxesExtractor
from BoundingBox import BoundingBox
import drawing_utils
import geometric_features as features
import color_utils
import time
import img_proc

MIN_BOUNDING_BOX_AREA = 250
ASPECT_RATIO_UPPER_BOUND = 3.2
ASPECT_RATIO_LOWER_BOUND = 2.3


def process(image: str):
    input_images_path = 'images/'

    bgr_image = cv2.imread(input_images_path + image)
    hsv_image = color_utils.bgr2hsv(bgr_image)
    thresholded_image = img_proc.threshold(hsv_image)
    closed_image = img_proc.close(thresholded_image, 5, 3)

    cv2.imwrite('intermediate/thresholded/{}'.format(image), closed_image)

    all_bounding_boxes = BoundingBoxesExtractor(closed_image).get_bounding_boxes()
    valid_bounding_boxes = filter_out_bounding_boxes(all_bounding_boxes, closed_image, image)

    drawing_utils.draw_bounding_boxes(bgr_image, valid_bounding_boxes)

    out_path = 'output/{}'.format(image)
    cv2.imwrite(out_path, bgr_image)


def filter_out_bounding_boxes(bounding_boxes: List[BoundingBox], closed_image: np.ndarray, image: str):
    valid_bounding_boxes = []
    for idx, bounding_box in enumerate(bounding_boxes):
        if ASPECT_RATIO_LOWER_BOUND <= bounding_box.get_aspect_ratio() <= ASPECT_RATIO_UPPER_BOUND \
                and bounding_box.get_box_area() > MIN_BOUNDING_BOX_AREA:
            image_path = 'intermediate/boxes/{}{}.png'.format(idx, image)
            box_image = bounding_box.get_from_image(closed_image)
            cv2.imwrite(image_path, box_image)
            if features.is_lot_logo(box_image, image_path):
                valid_bounding_boxes.append(bounding_box)
    return valid_bounding_boxes


if __name__ == '__main__':
    start = time.time()
    images = ['dwa.jpg', 'dwa2.png', 'dwa3.png', '11.png', 'lot2.jpg', 'lot3.jpg', 'lot5.jpg']
    for image in images:
        process(image)
    end = time.time()
    print('elapsed time: {}'.format(end - start))