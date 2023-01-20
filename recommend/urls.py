from . import views
from django.urls import path, include

urlpatterns = [
    path('saveteamandmenu/', views.saveTeamAndMenu, name='saveteamandmenu'), 
    path('teamlist/', views.teamList, name='teamlist'),
    path('todaycafeteria/', views.todayCafeteria, name='todaycafeteria')
]
