import numpy as np
from numba import njit

HUE_LOWER_BOUND = 108
HUE_HIGHER_BOUND = 125
SATURATION_LOWER_BOUND = 70
SATURATION_HIGHER_BOUND = 255
VALUE_LOWER_BOUND = 20
VALUE_HIGHER_BOUND = 255


def threshold(hsv_image: np.ndarray):
    hsv_image[np.where(np.logical_not(np.logical_and(hsv_image >= [HUE_LOWER_BOUND, SATURATION_LOWER_BOUND, VALUE_LOWER_BOUND],
                                                     hsv_image <= [HUE_HIGHER_BOUND, SATURATION_HIGHER_BOUND, VALUE_HIGHER_BOUND]).all(axis=2)))] = 0

    hsv_image[np.where(np.logical_and(hsv_image >= [HUE_LOWER_BOUND, SATURATION_LOWER_BOUND, VALUE_LOWER_BOUND],
                                      hsv_image <= [HUE_HIGHER_BOUND, SATURATION_HIGHER_BOUND, VALUE_HIGHER_BOUND]).all(axis=2))] = 255

    return hsv_image[:, :, 0]


@njit
def close(image: np.ndarray, dilate_kernel: int, erode_kernel: int):
    return erode(dilate(image, dilate_kernel), erode_kernel)


@njit
def dilate(image: np.ndarray, kernel: int):
    kernel_low, kernel_hi = np.uint(kernel / 2), np.uint(kernel / 2 + 1)
    h, w = image.shape
    out = np.zeros(image.shape, np.uint8)
    for i in range(2, h - 2):
        for j in range(2, w - 2):
            neighbourhood = image[i - kernel_low:i + kernel_hi, j - kernel_low:j + kernel_hi]
            if np.any(neighbourhood == 255):
                out[i][j] = np.uint(255)
            else:
                out[i][j] = np.uint(0)
    return out


@njit
def erode(image: np.ndarray, kernel: int):
    kernel_low, kernel_hi = np.uint(kernel / 2), np.uint(kernel / 2 + 1)
    h, w = image.shape
    out = np.zeros(image.shape, np.uint8)
    for i in range(1, h - 1):
        for j in range(1, w - 1):
            neighbourhood = image[i - kernel_low:i + kernel_hi, j - kernel_low:j + kernel_hi]
            if not np.any(neighbourhood != 255):
                out[i][j] = np.uint(255)
            else:
                out[i][j] = np.uint(0)
    return out


