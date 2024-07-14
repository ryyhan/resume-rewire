from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('',views.smart_ats_view,name='home'),
]