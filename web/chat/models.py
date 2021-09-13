from django.db import models
from uuid import uuid4, uuid5
from . import managers

# Create your models here.

class Chat(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    name = models.CharField(max_length=100)


class UserChat(models.Model):
    user_id = models.PositiveIntegerField()
    chat = models.ForeignKey('Chat', on_delete=models.CASCADE, related_name='user_chat')

    class Meta:
        constraints=[
            models.UniqueConstraint(fields=['user_id', 'chat'], name='unique_user_in_chat')
        ]

class Message(models.Model):
    author_id = models.PositiveIntegerField()
    content = models.TextField(max_length=1000)
    chat = models.ForeignKey('Chat', on_delete=models.CASCADE, related_name='messages')
    date = models.DateTimeField(auto_now_add=True, db_index=True)

