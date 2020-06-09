"""car_value_predictor URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from license_detector.views import get_license
from color_detector.views import detect_color
from car_details.views import get_details
from predictor.views import get_prediction


urlpatterns = [
    path('license_detection/detect/', get_license),
    path('color_detection/detect_color/', detect_color),
    path('car_details/detect/', get_details),
    path('predictor/detect/', get_prediction),
    path('admin/', admin.site.urls),
]
