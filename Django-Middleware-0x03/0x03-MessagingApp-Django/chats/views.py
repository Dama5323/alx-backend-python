from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action  

from .models import Conversation, Message
from .filters import MessageFilter
from .pagination import MessagePagination
from .serializers import (
    ConversationSerializer,
    ConversationCreateSerializer,
    MessageSerializer,
    MessageCreateSerializer
)
from .permissions import IsParticipant, IsParticipantOfConversation


class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling Conversations with JWT authentication.
    Users can only access conversations they participate in.
    """
    permission_classes = [IsAuthenticated, IsParticipant]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['updated_at']
    ordering = ['-updated_at']
    lookup_field = 'conversation_id'
    serializer_class = ConversationSerializer
    
    def get_serializer_class(self):
        if self.action == 'create':
            return ConversationCreateSerializer
        return ConversationSerializer

    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user)

    def perform_create(self, serializer):
        conversation = serializer.save()
        conversation.participants.add(self.request.user)

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.check_object_permissions(request, instance)
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except Exception:
            return Response(
                {"detail": "Not found or permission denied"}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
    @action(detail=True, methods=['put', 'patch'])
    def update_conversation(self, request, conversation_id=None):
        conversation = get_object_or_404(Conversation, id=conversation_id)
        if not conversation.participants.filter(id=request.user.id).exists():
            return Response(
                {"detail": "You are not a participant of this conversation"},
                status=status.HTTP_403_FORBIDDEN
            )
class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling Messages with JWT authentication.
    Users can only access messages from conversations they participate in.
    Includes pagination, filtering, and ordering.
    """
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filterset_class = MessageFilter
    pagination_class = MessagePagination
    ordering_fields = ['sent_at']
    ordering = ['-sent_at']

    def get_serializer_class(self):
        if self.action == 'create':
            return MessageCreateSerializer
        return MessageSerializer

    def get_queryset(self):
        return Message.objects.filter(
            Q(conversation__participants=self.request.user) |
            Q(sender=self.request.user)
        ).distinct()

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            if not (instance.conversation.participants.filter(id=request.user.id).exists() and 
                   instance.sender == request.user):
                return Response(
                    {"detail": "You can only delete your own messages"},
                    status=status.HTTP_403_FORBIDDEN
                )
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception:
            return Response(
                {"detail": "Message not found or permission denied"},
                status=status.HTTP_403_FORBIDDEN
            )

