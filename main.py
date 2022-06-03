import cv2
import numpy as np
from BoundingBoxesExtractor import BoundingBoxesExtractor
import box_drawer as bdraw
import copy

alpha = 1.2 # Simple contrast control
beta = 20   # Simple brightness control


def new_main():
    resized_img = cv2.imread('temp.jpg')
    bounding_boxes_builder = BoundingBoxesExtractor()
    bounding_boxes_builder.builder(resized_img.shape[0], resized_img.shape[1])
    bounding_boxes_builder.append(resized_img, 255)

    print('All images input for BBB')
    boxes_built = bounding_boxes_builder.build()
    print(len(boxes_built))
    print(boxes_built[0].to_string())
    image = bdraw.draw_boxes(copy.copy(resized_img), boxes_built)
    cv2.imshow('image', image)
    # cv2.imwrite('4_segmented/' + str(image_number) + '.jpg', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def print_hi(name):
    img = cv2.imread('images/11.jpg')
    img = cv2.GaussianBlur(img, (5, 5), 0)
    # img = resize(img)
    # white_balanced = white_balance(img)
    # cv2.imshow('white_balanced', white_balanced)
    # blurred = cv2.blur(white_balanced, (3, 3))

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    thresholded = threshold(hsv)
    close(thresholded)
    # brighter = brighten(blurred)
    #
    cv2.imshow('original', img)
    # cv2.imshow('hist equalized', img_output)
    cv2.imshow('thresholded', thresholded)

    # cv2.imshow('brighten', brighter)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# def close(img):
#     kernel = np.ones((5, 5), np.uint8)
#     closing = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
#     cv2.imshow('closed', closing)
#     cv2.imwrite('temp.jpg', closing)

def close(img):
    kernel5 = np.ones((5, 5), np.uint8)
    kernel7 = np.ones((5, 5), np.uint8)
    closing = cv2.erode(img, kernel5)

    closing = cv2.dilate(img, kernel7)
    # closing = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
    cv2.imshow('closed', closing)
    cv2.imwrite('temp.jpg', closing)

def white_balance(img):
    result = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    avg_a = np.average(result[:, :, 1])
    avg_b = np.average(result[:, :, 2])
    result[:, :, 1] = result[:, :, 1] - ((avg_a - 128) * (result[:, :, 0] / 255.0) * 1.1)
    result[:, :, 2] = result[:, :, 2] - ((avg_b - 128) * (result[:, :, 0] / 255.0) * 1.1)
    result = cv2.cvtColor(result, cv2.COLOR_LAB2BGR)
    return result


def brighten(image):
    new_image = np.zeros(image.shape, image.dtype)
    for y in range(image.shape[0]):
        for x in range(image.shape[1]):
            for c in range(image.shape[2]):
                new_image[y, x, c] = np.clip(alpha * image[y, x, c] + beta, 0, 255)
    return new_image


def threshold(hsv):
    h_low = 108
    h_hi = 125
    s_low = 0.3
    s_hi = 1
    v_low = 0.1
    v_hi = 1
    threshold = cv2.inRange(hsv, (h_low, s_low * 255, v_low * 255), (h_hi, s_hi * 255, v_hi * 255))
    return threshold


def resize(img: str):
    scale_percent = 40  # percent of original size
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)

    # resize image
    return cv2.resize(img, dim, interpolation=cv2.INTER_AREA)


if __name__ == '__main__':
    new_main()
