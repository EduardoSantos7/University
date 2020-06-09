import cv2
import numpy as np


class Preprocessor:
    @staticmethod
    def preprocess(path):
        image = cv2.imread(path)
        image = Preprocessor.erase_background(image)
        return image

    @staticmethod
    def erase_background(image):
        mask = np.zeros(image.shape, dtype=np.uint8)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        thresh = cv2.threshold(
            gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
        opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=30)

        cnts = cv2.findContours(opening, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
        for c in cnts:
            cv2.drawContours(mask, [c], -3, (255, 255, 255), -1)
            break

        close = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=4)
        close = cv2.cvtColor(close, cv2.COLOR_BGR2GRAY)
        result = cv2.bitwise_and(image, image, mask=close)
        result[close == 0] = (255, 255, 255)
        return result

    @staticmethod
    def gray_blur_canny(image, kernel=(2, 2), canny_range=(30, 255), dialte_iter=4):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.blur(gray, kernel)
        canny = cv2.Canny(gray, *canny_range)
        canny = cv2.dilate(canny, None, iterations=dialte_iter)
        return gray, canny

    @staticmethod
    def crop_image(image, box):
        return image[box.get('top', 0):box.get('bottom', 0), box.get('left', 0): box.get('right', 0)]
