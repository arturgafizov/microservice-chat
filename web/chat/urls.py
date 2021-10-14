from django.urls import path
from django.conf import settings
from django.views.generic import TemplateView

from rest_framework.routers import DefaultRouter

from . import views
from .views import ChatInitView

app_name = 'chat'

router = DefaultRouter()

urlpatterns = [
    # path('short/info/<pk>/', views.ShortUserInfoView.as_view(), name='short_user_info'),
    path('chat/list/', views.ChatListView.as_view(), name='chat_list_user'),
    path('message/<chat_id>/', views.MessageListView.as_view(), name='message_list_user'),
    path('init/', ChatInitView.as_view(), name='init_template'),
    path('jwt/', TemplateView.as_view(template_name='chat/init.html'), name='jwt_user'),
    # path('sign-in/info/<pk>/', views.UserSignInInfoView.as_view(), name='user_sign_in_info'),
    # path('sign-up/info/<pk>/', views.UserSignUpInfoView.as_view(), name='user_sign_up_info'),
]

urlpatterns += router.urls
urlpatterns += [
    path('profiles/profile/short/<pk>/', TemplateView.as_view(), name='short_user_info'),
    path('profiles/profile/short/', TemplateView.as_view(), name='list_short_user_info'),
    path('auth/sign-in/info/<pk>/', TemplateView.as_view(), name='user_sign_in_info'),
    path('auth/sign-up/info/<pk>/', TemplateView.as_view(), name='user_sign_up_info'),
    path('user/jwt/', TemplateView.as_view(), name='user_jwt'),
]
