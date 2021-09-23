from rest_framework import serializers
from django.contrib.auth import get_user_model
# Create your serializers here.
from chat.models import Chat, UserChat


class  UserChatSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserChat
        fields = ('user_id', )


class ChatSerializer(serializers.ModelSerializer):
    user_chat = UserChatSerializer(many=True)

    class Meta:
        model = Chat
        fields = ('id', 'name', 'user_chat')
