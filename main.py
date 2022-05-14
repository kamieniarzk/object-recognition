import cv2

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.
    img = cv2.imread('images/test.jpg')
    img = cv2.resize(img, (400, 400))
    cv2.imshow('test', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    print_hi('PyCharm')
