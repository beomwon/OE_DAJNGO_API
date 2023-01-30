from django.urls import path
from . import views

urlpatterns = [
    # path('signup/', views.signUp, name='signup'), 
    path('login/', views.login, name='login'), 
    # path('cookie/', views.cookie, name='cookie'), 
    # path('logout/', views.logout, name='logout'), 
    path('insertfoodpreference/', views.insertFoodPreference, name='insertfoodpreference'),  
    path('deletefoodpreference/', views.deleteFoodPreference, name='deletefoodpreference'),
    path('myfoodpreferencelist/', views.myFoodPreferenceList, name='insertfoodpreference'),  
    path('myteamandmenu/', views.myTeamAndMenu, name='myteamandmenu'),
    path('mymustfoodlist/', views.myMustFoodList, name='mymustfoodlist'),
    path('insertmustfood/', views.insertMustFood, name='insertmustfood'),  
    path('deletemustfood/', views.deleteMustFood, name='insertmustfood'),  
    path('updatemustfood/', views.updateMustFood, name='updatemustfood'),  
    # path('test/', views.test, name='test'), 
    # path('testlogin/', views.testlogin, name='testlogin'),
    path('cookie/', views.cookie, name='cookie')
    # path('code/<str:email>', views.mailVerificationCode, name='code') 
]
