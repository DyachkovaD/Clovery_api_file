from django.urls import path

from files.views import *

urlpatterns = [
    path('', FileView.as_view(), name='files-list'),
    # path('<int:pk>/', FileViewDetail.as_view(), name='files-detail'),

]