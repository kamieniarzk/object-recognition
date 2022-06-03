import cv2
import numpy as np
import math


def calculate_and_write_coefficients_to_file(image_file_name: str, image_file_extension: str):
    input_file_name = 'images/' + image_file_name + image_file_extension
    output_file_name = 'coefficients/' + image_file_name + 'txt'
    img = cv2.imread(input_file_name, cv2.IMREAD_GRAYSCALE)
    coefficients = Coefficients(img)
    coefficients.write_to_file(output_file_name)


def get_perimeter_and_area(img: np.ndarray):
    perimeter = 0
    area = 0
    h, w = img.shape

    for y in range(1, w - 1):
        for x in range(1, h - 1):
            if get_brightness(img[x, y]) > 128:
                area += 1
            neighbourhood = img[x-1:x+2, y-1:y+2]
            if is_edge(neighbourhood):
                perimeter += 1

    return perimeter, area


def get_area(img: np.ndarray):
    area = 0
    h, w = img.shape

    for y in range(0, w):
        for x in range(0, h):
            if get_brightness(img[x, y]) > 128:
                area += 1

    return area


def get_brightness(pixel: np.array):
    return np.average(pixel)


def is_edge(kernel: np.ndarray):
    center_brightness = kernel[1, 1]
    h, w = kernel.shape

    for y in range(0, w):
        for x in range(0, h):
            if kernel[x, y] != center_brightness:
                return True

    return False


def get_perimeter(img: np.ndarray):
    perimeter = 0
    h, w = img.shape

    for y in range(1, w - 1):
        for x in range(1, h - 1):
            neighbourhood = img[x-1:x+2, y-1:y+2]
            if is_edge(neighbourhood):
                perimeter += 1

    return perimeter


def is_edge(neighbourhood: np.ndarray):
    center_pixel = neighbourhood[1, 1]
    return np.any(neighbourhood[:, :] != center_pixel)


def get_m_p_q(img: np.ndarray, p: int, q: int):
    m = 0
    h, w = img.shape

    for j in range(0, w - 1):
        for i in range(0, h - 1):
            binary_val = 0 if img[i, j] > 128 else 1
            m += (i ** p) * (j ** q) * binary_val

    return m


def get_moments(img: np.ndarray):
    m00 = get_m_p_q(img, 0, 0)
    m10 = get_m_p_q(img, 1, 0)
    m20 = get_m_p_q(img, 2, 0)
    m30 = get_m_p_q(img, 3, 0)
    m01 = get_m_p_q(img, 0, 1)
    m02 = get_m_p_q(img, 0, 2)
    m03 = get_m_p_q(img, 0, 3)
    m11 = get_m_p_q(img, 1, 1)
    m12 = get_m_p_q(img, 1, 2)
    m21 = get_m_p_q(img, 2, 1)
    i = m10 / m00
    j = m01 / m00

    M00 = m00
    M01 = m01 - (m01 / m00) * m00
    M10 = m10 - (m10 / m00) * m00
    M11 = m11 - m10 * m01 / m00
    M20 = m20 - (m10 ** 2 / m00)
    M02 = m02 - (m10 ** 2 / m00)
    M21 = m21 - 2 * m11 * i - m20 * j + 2 * m01 * i ** 2
    M12 = m12 - 2 * m11 * j - m02 * i + 2 * m10 * j ** 2
    M30 = m30 - 3 * m20 * i + 2 * m10 * i ** 2
    M03 = m03 - 3 * m02 * j + 2 * m01 * j ** 2
    M1 = (M20 + M02) / m00 ** 3
    M2 = (M20 - M02) ** 2 + 4 * M11 ** 2 / m00 ** 4
    M3 = (M30 - 3 * M12) ** 2 + (3 * M21 - M03) ** 2 / m00 ** 6
    M4 = (M30 - M12) ** 2 + (M21 + M03) ** 2 / m00 ** 5
    M5 = ((M30 - 3 * M12) * (M30 + M12) * ((M30 + M12) ** 2) - 3 * ((M21 + M03) ** 2)  + (3 * M21 - M03) * (M21 + M03) * (3 * (M30 + M12) ** 2 - (M21 + M03) ** 2)) / m00 ** 10
    M6 = ((M20 - M02) * ((M30 + M12) ** 2 - (M21 + M03) ** 2) + 4 * M11 * (M30 + M12) * (M21 + M03)) / m00 ** 7
    M7 = (M20 * M02 - M11 ** 2) /m00 ** 4
    M8 = (M30 * M12 + M21 * M03 - M12 ** 2 - M21 ** 2) / m00 ** 5
    M9 = (M20 * (M21 * M03 - M12 ** 2) + M02 * (M02 * M12 - M21 ** 2) - M11 * (M30 * M03 - M21 * M12)) / m00 ** 7

    f = open('moments.txt', 'w')
    f.write('M1: {}\n'.format(M1))
    f.write('M2: {}\n'.format(M2))
    f.write('M3: {}\n'.format(M3))
    f.write('M4: {}\n'.format(M4))
    f.write('M5: {}\n'.format(M5))
    f.write('M6: {}\n'.format(M6))
    f.write('M7: {}\n'.format(M7))
    f.write('M8: {}\n'.format(M8))
    f.write('M9: {}\n'.format(M9))
    f.close()

    print(M1, M2, M3, M4, M5, M6, M7)


def get_w3(perimeter: int, area: int):
    return perimeter / (2 * math.sqrt(math.pi * area)) - 1


class Coefficients:
    def __init__(self, image: np.ndarray):
        self.image = image
        self.m00 = get_m_p_q(image, 0, 0)
        self.m10 = get_m_p_q(image, 1, 0)
        self.m20 = get_m_p_q(image, 2, 0)
        self.m30 = get_m_p_q(image, 3, 0)
        self.m01 = get_m_p_q(image, 0, 1)
        self.m02 = get_m_p_q(image, 0, 2)
        self.m03 = get_m_p_q(image, 0, 3)
        self.m11 = get_m_p_q(image, 1, 1)
        self.m12 = get_m_p_q(image, 1, 2)
        self.m21 = get_m_p_q(image, 2, 1)
        self.i = self.m10 / self.m00
        self.j = self.m01 / self.m00
        self.M00 = self.m00
        self.M01 = self.m01 - (self.m01 / self.m00) * self.m00
        self.M10 = self.m10 - (self.m10 / self.m00) * self.m00
        self.M11 = self.m11 - self.m10 * self.m01 / self.m00
        self.M20 = self.m20 - (self.m10 ** 2 / self.m00)
        self.M02 = self.m02 - (self.m10 ** 2 / self.m00)
        self.M21 = self.m21 - 2 * self.m11 * self.i - self.m20 * self.j + 2 * self.m01 * self.i ** 2
        self.M12 = self.m12 - 2 * self.m11 * self.j - self.m02 * self.i + 2 * self.m10 * self.j ** 2
        self.M30 = self.m30 - 3 * self.m20 * self.i + 2 * self.m10 * self.i ** 2
        self.M03 = self.m03 - 3 * self.m02 * self.j + 2 * self.m01 * self.j ** 2
        self.M1 = (self.M20 + self.M02) / self.m00 ** 2
        self.M2 = ((self.M20 - self.M02) ** 2 + 4 * self.M11 ** 2) / self.m00 ** 4
        self.M3 = ((self.M30 - 3 * self.M12) ** 2 + (3 * self.M21 - self.M03) ** 2) / self.m00 ** 5
        self.M4 = ((self.M30 + self.M12) ** 2 + (self.M21 + self.M03) ** 2) / self.m00 ** 5
        self.M5 = ((self.M30 - 3 * self.M12) * (self.M30 + self.M12) * (((self.M30 + self.M12) ** 2) - 3 *
                   ((self.M21 + self.M03) ** 2)) + (3 * self.M21 - self.M03) *
                   (self.M21 + self.M03) * (3 * (self.M30 + self.M12) ** 2 - (self.M21 + self.M03) ** 2)) / self.m00 ** 10
        self.M6 = ((self.M20 - self.M02) * ((self.M30 + self.M12) ** 2 - (self.M21 + self.M03) ** 2) + 4 * self.M11 *
                   (self.M30 + self.M12) * (self.M21 + self.M03)) / self.m00 ** 7
        self.M7 = (self.M20 * self.M02 - self.M11 ** 2) / self.m00 ** 4
        self.M8 = (self.M30 * self.M12 + self.M21 * self.M03 - self.M12 ** 2 - self.M21 ** 2) / self.m00 ** 5
        self.M9 = (self.M20 * (self.M21 * self.M03 - self.M12 ** 2) + self.M02 * (self.M02 * self.M12 - self.M21 ** 2) -
                   self.M11 * (self.M30 * self.M03 - self.M21 * self.M12)) / self.m00 ** 7
        self.perimeter, self.area = self.get_perimeter_and_area()
        self.W3 = self.get_w3()
        self.W4 = self.get_w4()

    def get_m_p_q(self, p: int, q: int):
        m = 0
        h, w = self.image.shape

        for j in range(0, w - 1):
            for i in range(0, h - 1):
                binary_val = 0 if self.image[i, j] > 128 else 1
                m += (i ** p) * (j ** q) * binary_val

        return m

    def get_perimeter_and_area(self):
        perimeter = 0
        area = 0
        h, w = self.image.shape

        for y in range(1, w - 1):
            for x in range(1, h - 1):
                if get_brightness(self.image[x, y]) > 128:
                    area += 1
                neighbourhood = self.image[x - 1:x + 2, y - 1:y + 2]
                if is_edge(neighbourhood):
                    perimeter += 1

        return perimeter, area

    def get_w4(self):
        sum = 0
        h, w = self.image.shape

        for j in range(0, w - 1):
            for i in range(0, h - 1):
                sum += self.get_distance_to_center([i, j]) ** 2

        return self.area / math.sqrt(2 * math.pi * sum)

    def get_w3(self):
        return self.perimeter / (2 * math.sqrt(math.pi * self.area)) - 1

    def get_distance_to_center(self, point):
        return math.sqrt((point[0] - self.i) ** 2 + (point[1] - self.j) ** 2)

    def write_to_file(self, file_name: str):
        f = open(file_name, 'w')
        f.write('M1: {0:.10f}\n'.format(self.M1))
        f.write('M2: {0:.10f}\n'.format(self.M2))
        f.write('M3: {0:.10f}\n'.format(self.M3))
        f.write('M4: {0:.10f}\n'.format(self.M4))
        f.write('M5: {0:.10f}\n'.format(self.M5))
        f.write('M6: {0:.10f}\n'.format(self.M6))
        f.write('M7: {0:.10f}\n'.format(self.M7))
        f.write('M8: {0:.10f}\n'.format(self.M8))
        f.write('M9: {0:.10f}\n'.format(self.M9))
        f.write('W3: {0:.10f}\n'.format(self.W3))
        f.write('W4: {0:.10f}\n'.format(self.W4))
        f.write('Perimeter: {0:.10f}\n'.format(self.perimeter))
        f.write('Area: {0:.10f}\n'.format(self.area))
        f.write('Perimeter/area ratio: {0:.10f}'.format(self.perimeter / self.area))
        f.close()


if __name__ == '__main__':
    calculate_and_write_coefficients_to_file('double2b', '.png')