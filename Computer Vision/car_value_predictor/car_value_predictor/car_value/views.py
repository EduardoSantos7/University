from django.shortcuts import render

# Create your views here.
# import the necessary packages
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import numpy as np
import urllib
import json
import cv2

from .linear_model import predict


@csrf_exempt
def detect(request):
    # initialize the data dictionary to be returned by the request
    data = {"success": False}
    car = []
    # check to see if this is a post request
    if request.method == "POST":
        if request.POST.get("car", ""):
            car = eval(request.POST.get("car", []))
            print(car, type(car))

        value = predict(car)

        data["value"] = value[0]
        data["success"] = True if value else False
    # return a JSON response
    return JsonResponse(data)
