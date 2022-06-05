import numpy as np
from numba import njit


@njit
def bgr2hsv(image: np.ndarray):
    rows, cols, channels = image.shape
    image = image.astype(np.float64)
    for i in range(0, rows):
        for j in range(0, cols):
            image[i, j] = bgr_to_hsv(image[i, j])
    return image


@njit
def bgr_to_hsv(pixel: np.ndarray):
    r_dash = pixel[2] / 255
    g_dash = pixel[1] / 255
    b_dash = pixel[0] / 255

    c_max = max(r_dash, g_dash, b_dash)
    c_min = min(r_dash, g_dash, b_dash)
    delta = c_max - c_min

    if delta == 0:
        H = 0
    elif c_max == r_dash:
        H = (60 * (((g_dash - b_dash) / delta) % 6))
    elif c_max == g_dash:
        H = (60 * (((b_dash - r_dash) / delta) + 2))
    elif c_max == b_dash:
        H = (60 * (((r_dash - g_dash) / delta) + 4))

    if c_max == 0:
        S = 0
    else:
        S = delta / c_max
    V = c_max

    return [int(H / 2), int(S * 255), int(V * 255)]