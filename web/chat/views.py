import logging
from django.utils.translation import gettext_lazy as _
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import GenericAPIView, UpdateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.reverse import reverse_lazy
from rest_framework.permissions import AllowAny
from main.service import BlogMicroService
from chat import serializers
from main.views import TemplateAPIView
from . import services
from . import serializers
from django.shortcuts import render

from .models import Chat, Message
from .services import ChatService
from main.pagination import BasePageNumberPagination
logger = logging.getLogger(__name__)

# Create your views here.

class Index(ListAPIView):
    def get(self, request):
        return render(self.request, 'chat/index.html', {})


class Room(ListAPIView):
    def get(self, request, room_name):
        return render(self.request, 'chat/room.html', {
            'room_name': room_name
    })


class ShortUserInfoView(UpdateAPIView):
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
        return service.service_response()


class ListShortUserInfoView(GenericAPIView):
    # serializer_class = ShortUserInfoSerializer

    def get(self, request):
        url = reverse_lazy('chat:list_short_user_info')
        service = BlogMicroService(request, url)
        return service.service_response()


class ChatListView(ListAPIView):
    serializer_class = serializers.ChatSerializer
    pagination_class = BasePageNumberPagination

    def get_queryset(self):
        print(self.request.remote_user)
        return ChatService.get_user_chat(self.request.remote_user)


class MessageListView(ListAPIView):
    serializer_class = serializers.MessageSerializer
    pagination_class = BasePageNumberPagination

    def get_queryset(self):
        return ChatService.get_messages(self.kwargs['chat_id'])


class ChatInitView(GenericAPIView):
    template_name = 'chat/init.html'
    permission_classes = (AllowAny, )
    serializer_class = serializers.ChatInitSerializer

    def get(self, request):
        return Response()

    def post(self, request):
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = Response(serializer.user_data)
        ChatService.set_jwt_access_cookie(response, serializer.validated_data['jwt'])
        return response
