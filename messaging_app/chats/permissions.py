from rest_framework import permissions  
from rest_framework.permissions import BasePermission, IsAuthenticated
from .models import Conversation

class IsParticipantOfConversation(IsAuthenticated):
    """
    Custom permission to only allow:
    - Authenticated users
    - Participants of the conversation
    """
    def has_object_permission(self, request, view, obj):
        # First check if user is authenticated (parent class)
        if not super().has_permission(request, view):
            return False

        # For Conversation objects
        if isinstance(obj, Conversation):
            return obj.participants.filter(id=request.user.id).exists()

        # For Message objects
        return obj.conversation.participants.filter(id=request.user.id).exists()

class IsSenderOrParticipant(BasePermission):
    """Check if user is sender or conversation participant"""
    def has_object_permission(self, request, view, obj):
        return (request.user == obj.sender) or (request.user in obj.conversation.participants.all())
