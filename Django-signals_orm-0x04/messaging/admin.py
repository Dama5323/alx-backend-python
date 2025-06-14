from django.contrib import admin
from .models import Message, MessageHistory, Notification

class MessageHistoryInline(admin.TabularInline):
    model = MessageHistory
    extra = 0
    readonly_fields = ('edited_at',)
    can_delete = False


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'timestamp', 'short_content', 'edited', 'edited_at')
    list_filter = ('sender', 'receiver', 'timestamp','edited', 'timestamp', 'edited_at')
    search_fields = ('content', 'sender__username', 'receiver__username')
    inlines = [MessageHistoryInline]
    
    def short_content(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    short_content.short_description = 'Content'


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('user__username', 'message__content')
    

@admin.register(MessageHistory)
class MessageHistoryAdmin(admin.ModelAdmin):
    list_display = ('message', 'short_content', 'edited_at')
    readonly_fields = ('message', 'content', 'edited_at')
    
    def short_content(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    short_content.short_description = 'Content'