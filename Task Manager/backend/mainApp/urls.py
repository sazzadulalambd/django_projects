
from django.contrib import admin
from django.urls import path, include
from . import views
from rest_framework import routers

from django.conf import settings
from django.conf.urls.static import static

router = routers.DefaultRouter()
router.register(r'teams', views.TeamView, 'team')

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('', views.index, name='index'),
    path('login/', views.LoginAPI.as_view()),
    path('register/', views.RegisterAPI.as_view()),
    path('profile/', views.account, name='profile'),
    path('api/', include(router.urls), name='TeamView'),
    path('tasks/', views.task_list, name='task-list'),
    path('task/<int:pk>/', views.task_detail, name='task-detail'),
    path('task/<int:pk>/pdf/', views.GeneratePdf.as_view(), name='GeneratePdf'),


]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# path('tasks/', views.alltasks, name='alltasks'),
# path('task/<int:pk>/', views.task, name='task'),
# path('task/', views.create, name='create'),
# path('task-update/<int:pk>/', views.update, name='update'),
# path('task-delete/<int:pk>/', views.delete, name='delete'),
