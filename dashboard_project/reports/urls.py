from django.urls import path
from . import views

urlpatterns = [
    path('', views.ReportsIndex, name='ReportsIndex'),
    path('<str:username>', views.ReportsIndex, name='ReportsIndex'),
    path('courselist/<str:username>/pdf', views.CourseListPDF, name='CourseListPDF'),
    path('courselist/<str:username>/csv', views.CourseListCSV, name='CourseListCSV'),
]
