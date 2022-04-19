from django.urls import path
from django.contrib import admin
from django.contrib import admin
from django.conf.urls import include
from wta import views

urlpatterns = [

    # The home page
    path('', views.update_db, name='update_db'),

]
