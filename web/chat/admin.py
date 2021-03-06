from django.contrib import admin

# Register your models here.
from . models import Chat, UserChat, Message


class UserChatInline(admin.TabularInline):
    model = UserChat
    extra = 0


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', )
    inlines = (UserChatInline, )
    readonly_fields = ('id', )


@admin.register(UserChat)
class UserChatAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'chat')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('author_id', 'content', 'chat', 'date')
