# chats/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Conversation, Message

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active')

admin.site.register(User, CustomUserAdmin)
admin.site.register(Conversation)
admin.site.register(Message)