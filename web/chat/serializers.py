from rest_framework import serializers
from django.contrib.auth import get_user_model
# Create your serializers here.
from chat.models import Chat, UserChat, Message
from . services import ChatService
from main.utils import find_dict_in_list


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
        print(user_chat)
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

    class Meta:
        model = Message
        fields = ('author_id', 'content', 'chat', 'date')


class ChatInitSerializer(serializers.Serializer):
    jwt = serializers.CharField()
    user_id = serializers.IntegerField()

    def validate_jwt(self, jwt: str):
        self.user_data = ChatService.get_or_set_cache(self.context['request'], jwt)
        # print(self.user_data)
        return jwt

    def save(self):
        # print(self.validated_data)
        user_1 = self.user_data.get('id')
        user_2 = self.validated_data.get('user_id')
        # print(user_1, user_2)
        chat = ChatService.get_or_create_chat(user_1, user_2)
        print(chat)
