from rest_framework import serializers
from django.contrib.auth import get_user_model
# Create your serializers here.
from chat.models import Chat, UserChat, Message
from . services import ChatService
from main.utils import find_dict_in_list
from dataclasses import asdict


class UserChatSerializer(serializers.ModelSerializer):
    user_data = serializers.SerializerMethodField('get_user_data')
    # user_data = serializers.IntegerField()

    class Meta:
        model = UserChat
        fields = ('user_id', 'user_data', )

    def get_user_data(self, obj) -> dict:
        # print(obj.user_id)
        return find_dict_in_list(self.context['user_data'], 'id', obj.user_id)

    def to_representation(self, instance):
        # find_dict_in_list(self.context['user_data'], 'id', instance.user_id)
        data = super().to_representation(instance)
        user_chat = data['user_data']
        # print(user_chat)
        return user_chat


class ChatSerializer(serializers.ModelSerializer):
    user_chat = serializers.SerializerMethodField('get_user_chat')
    last_message = serializers.SerializerMethodField('get_last_message')
    update_date = serializers.SerializerMethodField('get_update_date')

    class Meta:
        model = Chat
        fields = ('id', 'name', 'user_chat', 'last_message', 'update_date')

    def get_last_message(self, obj):
        return obj.last_message

    def get_update_date(self, obj):
        return obj.update_date

    def get_user_chat(self, obj):
        # print(self.context)
        return UserChatSerializer(obj.user_chat, many=True, context=self.context).data


class MessageSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField('get_author')

    class Meta:
        model = Message
        fields = ('author_id', 'content', 'chat', 'date', 'author')

    def get_author(self, obj):
        print(obj)
        users = ChatService.post_users_id([obj.author_id])
        return users[0]


class ChatInitSerializer(serializers.Serializer):
    jwt = serializers.CharField()
    user_id = serializers.IntegerField()

    def validate_jwt(self, jwt: str):
        # print('JWT', jwt)
        self.user_data = ChatService.get_or_set_cache(jwt)
        # print(self.user_data)
        return jwt

    def save(self):
        user_1 = self.user_data.id
        user_2 = self.validated_data.get('user_id')
        chat = ChatService.get_or_create_chat(user_1, user_2)
        print(chat)
