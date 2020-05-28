import cv2
import pytesseract

from utils.preprocessor import Preprocessor
from utils.ocr.license import extract_license
import time

from concurrent.futures import ProcessPoolExecutor, as_completed, wait


def get_license_plate():
    image = cv2.imread('toyota.jpg')
    image = cv2.resize(image, (800, 800))
    gray, canny = Preprocessor.gray_blur_canny(image)

    _, cnts, _ = cv2.findContours(canny, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    for c in cnts:
        area = cv2.contourArea(c)

        x, y, w, h = cv2.boundingRect(c)
        epsilon = 0.09*cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, epsilon, True)

        if len(approx) == 4 and area > 8000:
            print('area=', area)
            # cv2.drawContours(image,[approx],0,(0,255,0),3)

            aspect_ratio = float(w)/h

            if aspect_ratio > 2.2:
                placa = gray[y:y+h, x:x+w]
                text = pytesseract.image_to_string(placa, config='--psm 7')
                text2 = pytesseract.image_to_string(placa, config='--psm 6')
                text3 = pytesseract.image_to_string(placa, config='--psm 11')
                text4 = pytesseract.image_to_string(placa, config='--psm 13')
                print('PLACA: ', extract_license(text))

                # cv2.imshow('PLACA', placa)
                # cv2.moveWindow('PLACA', 780, 10)
                # cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 3)
                # cv2.putText(image, text, (x-20, y-10), 1, 2.2, (0, 255, 0), 3)

    # cv2.imshow('Image', image)
    # cv2.moveWindow('Image', 45, 10)
    # cv2.waitKey(0)


def get_license_plate_p():
    image = cv2.imread('toyota.jpg')
    image = cv2.resize(image, (800, 800))
    gray, canny = Preprocessor.gray_blur_canny(image)

    _, cnts, _ = cv2.findContours(
        canny, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    for c in cnts:
        area = cv2.contourArea(c)

        x, y, w, h = cv2.boundingRect(c)
        epsilon = 0.09*cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, epsilon, True)

        if len(approx) == 4 and area > 8000:
            print('area=', area)
            # cv2.drawContours(image,[approx],0,(0,255,0),3)

            aspect_ratio = float(w)/h

            if aspect_ratio > 2.2:
                placa = gray[y:y+h, x:x+w]
                with ProcessPoolExecutor() as executor:
                    psms = ['--psm 7', '--psm 6', '--psm 11', '--psm 13']
                    results = [executor.submit(orc, placa, psm) for psm in psms]

                    for f in as_completed(results):
                        if f.result():
                            print('PLACA: ', extract_license(f.result()))

                # cv2.imshow('PLACA', placa)
                # cv2.moveWindow('PLACA', 780, 10)
                # cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 3)
                # cv2.putText(image, text, (x-20, y-10), 1, 2.2, (0, 255, 0), 3)


    # cv2.imshow('Image', image)
    # cv2.moveWindow('Image', 45, 10)
    # cv2.waitKey(0)


def op(c, gray):
    area = cv2.contourArea(c)

    x, y, w, h = cv2.boundingRect(c)
    epsilon = 0.09*cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, epsilon, True)

    if len(approx) == 4 and area > 8000:
        print('area=', area)
        # cv2.drawContours(image,[approx],0,(0,255,0),3)

        aspect_ratio = float(w)/h

        if aspect_ratio > 2.2:
            placa = gray[y:y+h, x:x+w]
            with ProcessPoolExecutor() as executor:
                psms = ['--psm 7', '--psm 6', '--psm 11', '--psm 13']
                results = [executor.submit(orc, placa, psm) for psm in psms]

                for f in as_completed(results):
                    if f.result():
                        print('PLACA: ', extract_license(f.result()))

def orc(image, psm):
    return pytesseract.image_to_string(image, config=psm)

s = time.time()
get_license_plate()
e = time.time()

print(e - s)
