import cv2
import pytesseract

from utils.preprocessor import Preprocessor
from utils.ocr.license import extract_license
import time

from concurrent.futures import ProcessPoolExecutor, as_completed, wait


def get_license_plate(image_path, debug=True):
    image = cv2.imread(image_path)
    image = cv2.resize(image, (800, 800))
    gray, canny = Preprocessor.gray_blur_canny(image, kernel=(4, 4), canny_range=(10, 300))
    text_freq = {}
    license_plate = ""

    _, cnts, _ = cv2.findContours(
        canny, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    for c in cnts:
        area = cv2.contourArea(c)

        epsilon = 0.09*cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, epsilon, True)
        if area > 500 and debug:
            cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
            # show the output image
            cv2.imshow("Image", image)
            cv2.waitKey(0)
        # Process a rectangule
        if len(approx) > 1 and area > 2000:
            x, y, w, h = cv2.boundingRect(c)

            aspect_ratio = float(w)/h

            if aspect_ratio > 1.2:
                placa = gray[y:y+h, x:x+w]
                with ProcessPoolExecutor() as executor:
                    psms = ['--psm 7', '--psm 6', '--psm 11', '--psm 13']
                    results = [executor.submit(orc, placa, psm) for psm in psms]

                    for f in as_completed(results):
                        license_plate = extract_license(f.result())
                        # print(f.result(), "l ", license_plate, area, aspect_ratio, len(approx))
                        if license_plate:
                            text_freq[license_plate] = text_freq.get(license_plate, 0) + 1
                            if debug:
                                cv2.rectangle(
                                    image, (x, y), (x + w, y + h), (0, 255, 0), 3)
                                cv2.putText(image, license_plate, (x - 20, y - 10), 1, 2.2, (0, 255, 0), 3)
                if text_freq:
                    license_plate = max(text_freq, key=text_freq.get)

    return license_plate


def orc(image, psm):
    return pytesseract.image_to_string(image, config=psm)


def test_ocr():
    success = 0
    licenses = {
        'dodge': 'TZR-38-08',
        'dodge2': 'TZR-38-08',
        'ford': 'XWL-82-13',
        'ford2': 'UAF-31-31',
        'ford3': 'UAF-31-31',
        'ford4': 'UAF-31-31',
        'mazda': 'TZZ-97-38',
        'mazda2': 'TZZ-97-38',
        'nissan': 'XWH-61-96',
        'susuki': 'TPT-255-A',
        'toyota': 'TYU-83-38',
        'toyota2': 'TYU-83-38',
        'toyota3': 'TYU-83-38',
        'toyota4': 'TYU-83-38',
    }

    for brand, license_plate in licenses.items():
        text = get_license_plate(f'{brand}.jpg', debug=False)
        detected = text.replace(' ', '').replace('\n', '')
        print(detected, license_plate)
        if detected == license_plate:
            success += 1

    print(f'Average: {success/len(licenses.keys())}') 


test_ocr()
