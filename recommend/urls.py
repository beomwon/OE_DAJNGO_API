from . import views
from django.urls import path, include

urlpatterns = [
    path('teamlist/', views.teamList, name='teamlist'),
    path('todaycafeteria/', views.todayCafeteria, name='todaycafeteria'), 
    path('test/', views.test, name='test')
]
