import os
import cv2


class CarDetector():

    def __init__(self):
        self.car_back_path = os.path.join('images', 'templates', 'placa.jpg')
        self.car_front_path = os.path.join('images', 'templates', 'placa.jpeg')

    def check_face(self, image):
        car_front = cv2.imread(self.car_front_path, 0)
        car_back = cv2.imread(self.car_back_path, 0)
        front_d = cv2.matchShapes(car_front, image, cv2.CONTOURS_MATCH_I2, 0)
        back_d = cv2.matchShapes(car_back, image, cv2.CONTOURS_MATCH_I2, 0)
        # print(f'back: {back_d} front: {front_d}')

        return car_front if front_d < back_d else car_back

    def detect(self, image_path):
        # Read in grayscale
        image = cv2.imread(image_path, 0)

        # Detect if the input is the front/back face of the car
        template_image = self.check_face(image)

        top = self.detect_from_top(image, template_image)
        bottom = self.detect_from_bottom(image, template_image)
        right = self.detect_from_right(image, template_image)
        left = self.detect_from_left(image, template_image)

        if bottom - top <= 0:
            height, _ = image.shape[:2]
            top = 0
            bottom = height

        if right - left <= 0:
            _, width = image.shape[:2]
            left = 0
            right = width

        cropped = image[top:bottom, left: right]
        return {'top': top, 'bottom': bottom, 'left': left, 'right': right}
        #cv2.imwrite("out.jpg", cropped)

    def detect_from_top(self, image, template):
        sum_ = 0
        iter_ = 0
        start_y = 0
        height, width = image.shape[:2]
        for _ in range(0, 70):
            # Crop window of observation we defined above
            start_y += 10
            cropped = image[start_y:height, 0:width]

            d2 = cv2.matchShapes(template, cropped, cv2.CONTOURS_MATCH_I2, 0)
            sum_ += d2
            iter_ += 1
            average = sum_ / iter_

            if d2 - average > 0.1:
                break
        return start_y

    def detect_from_bottom(self, image, template):
        sum_ = 0
        iter_ = 0
        height, width = image.shape[:2]
        for _ in range(0, 70):
            # Crop window of observation we defined above
            height -= 10
            cropped = image[0:height, 0:width]

            d2 = cv2.matchShapes(template, cropped, cv2.CONTOURS_MATCH_I2, 0)
            sum_ += d2
            iter_ += 1
            average = sum_ / iter_

            if d2 - average > 0.1:
                break
        return height

    def detect_from_left(self, image, template):
        sum_ = 0
        iter_ = 0
        height, width = image.shape[:2]
        start_x = 0
        for _ in range(0, 70):
            # Crop window of observation we defined above
            start_x += 10
            cropped = image[0:height, start_x:width]

            d2 = cv2.matchShapes(template, cropped, cv2.CONTOURS_MATCH_I2, 0)
            sum_ += d2
            iter_ += 1
            average = sum_ / iter_

            if d2 - average > 0.001:
                break
        return start_x

    def detect_from_right(self, image, template):
        sum_ = 0
        iter_ = 0
        height, width = image.shape[:2]
        for _ in range(0, 70):
            # Crop window of observation we defined above
            width -= 10
            cropped = image[0:height, 0:width]

            d2 = cv2.matchShapes(template, cropped, cv2.CONTOURS_MATCH_I2, 0)
            sum_ += d2
            iter_ += 1
            average = sum_ / iter_

            if d2 - average > 0.001:
                break
        return width


c = CarDetector()
c.detect("images/ford.jpg")
