from django.urls import path
from . import views

urlpatterns = [
    path('enterstudents', views.EnterStudents, name='EnterStudents'),
]
