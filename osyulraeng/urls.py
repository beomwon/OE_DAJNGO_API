from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('user.urls')),
    path('store/', include('store.urls')),
    path('recommend/', include('recommend.urls'))
]
