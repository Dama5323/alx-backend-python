# chats/views.py
from django.db.models import Q
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from .models import Conversation, Message
from .serializers import (
    ConversationSerializer,
    ConversationCreateSerializer,
    MessageSerializer,
    MessageCreateSerializer
)
from .auth import IsParticipant  # ✅ Custom permission


class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling Conversations with JWT authentication.
    Users can only access conversations they participate in.
    """
    permission_classes = [IsAuthenticated, IsParticipant]  # ✅ Add custom permission
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['updated_at']
    ordering = ['-updated_at']

    def get_serializer_class(self):
        if self.action == 'create':
            return ConversationCreateSerializer
        return ConversationSerializer

    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user)

    def perform_create(self, serializer):
        conversation = serializer.save()
        conversation.participants.add(self.request.user)

class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling Messages with JWT authentication.
    Users can only access messages from conversations they participate in.
    """
    permission_classes = [IsAuthenticated, IsParticipant]  # ✅ Add custom permission
    filter_backends = [filters.OrderingFilter]
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

