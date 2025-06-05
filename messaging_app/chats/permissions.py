# messaging_app/chats/permissions.py
from rest_framework.permissions import BasePermission

class IsParticipant(BasePermission):
    """Check if user is a conversation participant"""
    def has_object_permission(self, request, view, obj):
        return request.user in obj.participants.all()

class IsSenderOrParticipant(BasePermission):
    """Check if user is sender or conversation participant"""
    def has_object_permission(self, request, view, obj):
        return (request.user == obj.sender) or (request.user in obj.conversation.participants.all())