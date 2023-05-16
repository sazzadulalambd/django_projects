
from django.contrib import admin
from django.urls import path, include
from . import views 
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'teams', views.TeamView,'team')

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('', views.index, name='index'),
    path('login/',views.LoginAPI.as_view()),
    path('register/',views.RegisterAPI.as_view()),
    path('api/', include(router.urls), name = 'TeamView'),
    path('tasks/', views.task_list, name='task-list'),
    path('task/<int:pk>/', views.task_detail, name='task-detail'),

]


# path('tasks/', views.alltasks, name='alltasks'),
# path('task/<int:pk>/', views.task, name='task'),
# path('task/', views.create, name='create'),
# path('task-update/<int:pk>/', views.update, name='update'),
# path('task-delete/<int:pk>/', views.delete, name='delete'),
