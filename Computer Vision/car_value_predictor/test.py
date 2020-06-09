import time

from ocr import get_license_plate
from crawler import Crawler
from parser import Parser


if __name__ == "__main__":
    s = time.time()

    image_path = 'images/ford.jpg'
    license_plate = get_license_plate(image_path)
    license_plate = license_plate.replace(' ', '').replace('-', '')

    crawler = Crawler()
    html = crawler.crawl(license_plate)

    parser = Parser(html)
    parser.process()

    e = time.time()

    print(parser.data)
    print(e - s)
