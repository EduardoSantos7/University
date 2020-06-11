from django.shortcuts import render
from .utils.preprocessor import Preprocessor
from .color import get_color
from .car_detector import CarDetector

# Create your views here.
# import the necessary packages
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import numpy as np
import urllib
import json
import cv2


@csrf_exempt
def detect_color(request):
    # initialize the data dictionary to be returned by the request
    data = {"success": False}

    # check to see if this is a post request
    if request.method == "POST":

        # check to see if an image was uploaded
        if request.FILES.get("image", None) is not None:
            # grab the uploaded image
            image = _grab_image(stream=request.FILES["image"])

        # if the input it's a path
        elif request.POST.get("path", None):
            image = request.POST.get("path", None)
            image = f"color_detector/{image}"
        # otherwise, assume that a URL was passed in
        else:
            # grab the URL from the request
            url = request.POST.get("url", None)
            # if the URL is None, then return an error
            if url is None:
                data["error"] = "No URL provided."
                return JsonResponse(data)
            # load the image and convert
            image = _grab_image(url=url)

        c = CarDetector()

        box = c.detect(image)

        if type(image) == str:
            # Read in grayscale
            image = cv2.imread(image, 0)

        car_focus = Preprocessor.crop_image(image, box)
        color = get_color(car_focus)

        data["color"] = color
        data["success"] = True if color else False
    # return a JSON response
    return JsonResponse(data)


def _grab_image(path=None, stream=None, url=None):
    # if the path is not None, then load the image from disk
    if path is not None:
        print("entre1")
        image = cv2.imread(path)
    # otherwise, the image does not reside on disk
    else:
        print("entre2")
        # if the URL is not None, then download the image
        if url is not None:
            resp = urllib.urlopen(url)
            data = resp.read()
        # if the stream is not None, then the image has been uploaded
        elif stream is not None:
            print("entre3")
            data = stream.read()
        # convert the image to a NumPy array and then read it into
        # OpenCV format
        image = np.asarray(bytearray(data), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)

    # return the image
    return image
