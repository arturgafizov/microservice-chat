import logging
from django.utils.translation import gettext_lazy as _
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.reverse import reverse_lazy

from main.service import BlogMicroService
from chat import serializers
from . import services
from . import serializers
from django.shortcuts import render
logger = logging.getLogger(__name__)

# Create your views here.

def index(request):
    return render(request, 'chat/index.html', {})

def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name': room_name
    })


class ShortUserInfoView(GenericAPIView):
    # serializer_class = ShortUserInfoSerializer

    def get(self, request, pk):
        url = reverse_lazy('chat:short_user_info', kwargs={'pk': pk})
        service = BlogMicroService(request, url)
        return service.service_response()


class UserSignInInfoView(GenericAPIView):
    # serializer_class = serializers.UserSignInInfoSerializer

    def get(self, request, pk):
        url = reverse_lazy('chat:user_sign_in_info', kwargs={'pk': pk})
        service = BlogMicroService(request, url)
        # print('Mistake', service)
        return service.service_response()


class UserSignUpInfoView(GenericAPIView):
    # serializer_class = serializers.UserSignInInfoSerializer

    def get(self, request, pk):
        url = reverse_lazy('chat:user_sign_up_info', kwargs={'pk': pk})
        service = BlogMicroService(request, url)
        # print('Mistake', service)
        return service.service_response()


class ListShortUserInfoView(GenericAPIView):
    # serializer_class = ShortUserInfoSerializer

    def get(self, request):
        url = reverse_lazy('chat:list_short_user_info')
        service = BlogMicroService(request, url)
        return service.service_response()
