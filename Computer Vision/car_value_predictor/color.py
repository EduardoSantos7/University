from scipy.spatial import distance as dist
import cv2
import numpy as np
import imutils
from collections import OrderedDict
from utils.preprocessor import Preprocessor


class ColorDetector:

    def __init__(self):
        # initialize the colors dictionary, containing the color
        # name as the key and the RGB tuple as the value
        colors = OrderedDict({
            "black": (10, 10, 10),
            "gray": (120, 120, 120),
            "white": (220, 220, 220),
            "red": (200, 30, 30),
            "green": (30, 210, 30),
            "blue": (30, 30, 210)})
        # allocate memory for the L*a*b* image, then initialize
        # the color names list
        self.lab = np.zeros((len(colors), 1, 3), dtype="uint8")
        self.colorNames = []
        # loop over the colors dictionary
        for (i, (name, rgb)) in enumerate(colors.items()):
            # update the L*a*b* array and the color names list
            self.lab[i] = rgb
            self.colorNames.append(name)
        # convert the L*a*b* array from the RGB color space
        # to L*a*b*
        self.lab = cv2.cvtColor(self.lab, cv2.COLOR_RGB2LAB)

    def label(self, image, c):
        # construct a mask for the contour, then compute the
        # average L*a*b* value for the masked region
        mask = np.zeros(image.shape[:2], dtype="uint8")
        cv2.drawContours(mask, [c], -1, 255, -1)
        mask = cv2.erode(mask, None, iterations=2)
        mean = cv2.mean(image, mask=mask)[:3]
        # initialize the minimum distance found thus far
        minDist = (np.inf, None)
        # loop over the known L*a*b* color values
        for (i, row) in enumerate(self.lab):
            # compute the distance between the current L*a*b*
            # color value and the mean of the image
            d = dist.euclidean(row[0], mean)
            # if the distance is smaller than the current distance,
            # then update the bookkeeping variable
            if d < minDist[0]:
                minDist = (d, i)
        # return the name of the color with the smallest distance
        return self.colorNames[minDist[1]]

cl = ColorDetector()

def get_color(image_path):
    image = cv2.imread(image_path)
    resized = cv2.resize(image, (800, 800))
    image = cv2.resize(image, (800, 800))
    ratio = image.shape[0] / float(resized.shape[0])
    gray, canny = Preprocessor.gray_blur_canny(image)
    color_area = {}

    _, cnts, _ = cv2.findContours(
        canny, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    for c in cnts:
        area = cv2.contourArea(c)

        epsilon = 0.09*cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, epsilon, True)
        # Process a rectangule

        if len(approx) <= 4 and area > 2_000 and area < 15_000:
            x, y, w, h = cv2.boundingRect(c)

            M = cv2.moments(c)
            cX = int((M["m10"] / M["m00"]) * ratio)
            cY = int((M["m01"] / M["m00"]) * ratio)
            # detect the shape of the contour and label the color
            color = cl.label(image, c)
            color_area[color] = color_area.get(color, 0) + area
            # multiply the contour (x, y)-coordinates by the resize ratio,
            # then draw the contours and the name of the shape and labeled
            # color on the image
            c = c.astype("float")
            c *= ratio
            c = c.astype("int")
            text = color
            cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
            cv2.putText(image, text, (cX, cY),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            # show the output image
            cv2.imshow("Image", image)
            cv2.waitKey(0)

    if color_area:
        return max(color_area, key=color_area.get)

    return ""

print(get_color("ford4.jpg"))
