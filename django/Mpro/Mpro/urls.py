from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('main.html', views.sub),
    path('main_A.html', views.main_A),
    path('main_B.html', views.main_B),
    path('main_C.html', views.main_C),
]