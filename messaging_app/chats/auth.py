# chats/auth.py

from rest_framework import permissions
from .models import Conversation

class IsParticipant(permissions.BasePermission):
    """
    Custom permission to allow only participants of a conversation to access it.
    """

    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'participants'):
            return request.user in obj.participants.all()
        return False
