from django.urls import path
from photos.views import *

urlpatterns = [
    path('', ImageInfoView.as_view(),),
]