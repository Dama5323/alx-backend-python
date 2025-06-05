# chats/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Conversation, Message

class UserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'online_status', 'last_seen')
    list_filter = ('online_status', 'is_staff', 'is_superuser')
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('profile_picture', 'bio', 'phone_number', 'online_status')}),
    )

admin.site.register(User, UserAdmin)
admin.site.register(Conversation)
admin.site.register(Message)