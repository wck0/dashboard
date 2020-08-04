from django.urls import path
from . import views

urlpatterns = [
    path('', views.Index, name='VitaIndex'),
    path('narrative', views.Narrative, name='VitaNarrative'),
    path('editnarrative', views.EditNarrative, name='VitaEditNarrative'),
    path('info/', views.Info, name='VitaInfo'),
    path('info/<str:username>', views.Info),
    path('application/', views.ApplicationView, name='VitaApplication'),
    path('application/<str:username>', views.ApplicationView),
    path('offcampus/', views.OffCampus, name='VitaOffCampus'),
    path('offcampus/<str:username>', views.OffCampus),
]

