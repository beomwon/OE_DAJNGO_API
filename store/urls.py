from django.urls import path
from . import views

urlpatterns = [
    path('storelist/', views.storeList, name='storelist'),  
    path('ratinglist/', views.ratingList, name='ratinglist'),
    path('insertrating/', views.insertRating, name='insertrating'),  
    path('updaterating/', views.updateRating, name='insertrating'),  
    path('deleterating/', views.deleteRating, name='deleterating'), 
    path('checktodayrating/', views.checkTodayRating, name='checktodayrating'),
    # path('cookie/', views.cookie, name='cookie'), 
    # path('logout/', views.logout, name='logout'),
    # path('code/<str:email>', views.mailVerificationCode, name='mailverificationcode')
]
