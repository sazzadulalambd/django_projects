from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.asset_index, name="asset_index"),
    path('create_asset', views.create_asset, name="create_asset"),
    
]