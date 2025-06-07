from rest_framework import permissions  
from rest_framework.permissions import BasePermission, IsAuthenticated
from .models import Conversation


class IsParticipant(BasePermission):
    """
    Allows access only to participants of the conversation.
    Used for ConversationViewSet.
    """
    def has_object_permission(self, request, view, obj):
        return request.user in obj.participants.all()


class IsParticipantOfConversation(BasePermission):
    """
    Custom permission that:
    1. Only allows authenticated users (checks user.is_authenticated)
    2. Only allows participants to access conversation/messages
    3. Handles all methods (GET, POST, PUT, PATCH, DELETE)
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        if request.method == 'POST':
            conversation_id = request.data.get('conversation')
            if conversation_id:
                return Conversation.objects.filter(
                    id=conversation_id,
                    participants=request.user
                ).exists()
            return True
            
        return True

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Conversation):
            return obj.participants.filter(id=request.user.id).exists()
        
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            return obj.conversation.participants.filter(id=request.user.id).exists()
        
        return obj.conversation.participants.filter(id=request.user.id).exists()


class IsSenderOrParticipant(BasePermission):
    """Check if user is sender or conversation participant"""
    def has_object_permission(self, request, view, obj):
        return (request.user == obj.sender) or (request.user in obj.conversation.participants.all())
