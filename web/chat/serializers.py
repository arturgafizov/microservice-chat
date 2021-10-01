from rest_framework import serializers
from django.contrib.auth import get_user_model
# Create your serializers here.
from chat.models import Chat, UserChat, Message
from . services import ChatService


class  UserChatSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserChat
        fields = ('user_id', )


class ChatSerializer(serializers.ModelSerializer):
    user_chat = UserChatSerializer(many=True)
    last_message = serializers.SerializerMethodField('get_last_message')
    update_date = serializers.SerializerMethodField('get_update_date')

    class Meta:
        model = Chat
        fields = ('id', 'name', 'user_chat' , 'last_message', 'update_date')

    def get_last_message(self, obj):
        return obj.last_message

    def get_update_date(self, obj):
        return obj.update_date


class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = ('author_id', 'content', 'chat', 'date')
