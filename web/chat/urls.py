from django.urls import path
from django.views.generic.base import TemplateView
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'chat'

router = DefaultRouter()

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:room_name>/', views.room, name='room'),
    path('short/info/<pk>/', views.ShortUserInfoView.as_view(), name='short_user_info')
]

urlpatterns += router.urls
urlpatterns += [
    path('profiles/profile/short/<pk>/', TemplateView.as_view(), name='short_user_info')
]
