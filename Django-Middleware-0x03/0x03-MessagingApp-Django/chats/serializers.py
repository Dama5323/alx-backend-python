# chats/serializers.py

from rest_framework import serializers
from .models import User, Conversation, Message

# 1. User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
        read_only_fields = ['id']


# 2. Nested Message Serializer for Conversations
class NestedMessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'sender', 'message_body', 'sent_at']


# 3. Full Message Serializer for Message views
class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'conversation', 'sender', 'message_body', 'sent_at']
        read_only_fields = ['sender', 'sent_at']

    def validate(self, data):
        """
        Additional validation to check if user is conversation participant
        """
        request = self.context.get('request')
        conversation = data.get('conversation') or self.instance.conversation
        
        if not conversation.participants.filter(id=request.user.id).exists():
            raise serializers.ValidationError(
                "You must be a participant of the conversation"
            )
        return data


# 4. Conversation Serializer with nested users/messages + latest message
class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = NestedMessageSerializer(many=True, read_only=True)
    latest_message = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['id', 'participants', 'created_at', 'latest_message', 'messages']

    def get_latest_message(self, obj):
        latest = obj.messages.order_by('-sent_at').first()
        return NestedMessageSerializer(latest).data if latest else None


# 5. Serializer to create conversation (with participant validation)
class ConversationCreateSerializer(serializers.ModelSerializer):
    participants = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=User.objects.all()
    )

    class Meta:
        model = Conversation
        fields = ['id', 'participants']

    def validate_participants(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("A conversation must include at least two participants.")
        return value

    def create(self, validated_data):
        participants = validated_data.pop('participants')
        conversation = Conversation.objects.create(**validated_data)
        conversation.participants.set(participants)
        return conversation


# 6. Serializer to create a message in a conversation (auth user must be participant)
class MessageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'conversation', 'message_body']

    def validate(self, data):
        user = self.context['request'].user
        if not data['conversation'].participants.filter(id=user.id).exists():
            raise serializers.ValidationError("You are not a participant in this conversation.")
        return data
