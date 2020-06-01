import cv2
import pytesseract

from utils.preprocessor import Preprocessor
from utils.ocr.license import extract_license
import time

from concurrent.futures import ProcessPoolExecutor, as_completed, wait


def get_license_plate(image_path):
    image = cv2.imread(image_path)
    image = cv2.resize(image, (800, 800))
    gray, canny = Preprocessor.gray_blur_canny(image)
    text_freq = {}

    _, cnts, _ = cv2.findContours(
        canny, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    for c in cnts:
        area = cv2.contourArea(c)

        epsilon = 0.09*cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, epsilon, True)
        # Process a rectangule
        if len(approx) == 4 and area > 8000:
            x, y, w, h = cv2.boundingRect(c)

            aspect_ratio = float(w)/h

            if aspect_ratio > 2.2:
                placa = gray[y:y+h, x:x+w]
                with ProcessPoolExecutor() as executor:
                    psms = ['--psm 7', '--psm 6', '--psm 11', '--psm 13']
                    results = [executor.submit(orc, placa, psm) for psm in psms]

                    for f in as_completed(results):
                        license_plate = extract_license(f.result())
                        if license_plate:
                            text_freq[license_plate] = text_freq.get(license_plate, 0) + 1

                license_plate = max(text_freq, key=text_freq.get)

    return license_plate


def orc(image, psm):
    return pytesseract.image_to_string(image, config=psm)
