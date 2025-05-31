# chats/serializers.py
from rest_framework import serializers
from .models import User, Conversation, Message
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError

class UserSerializer(serializers.ModelSerializer):
    # Adding requested CharField example
    full_name = serializers.CharField(
        source='get_full_name',
        read_only=True,
        help_text="User's full name"
    )
    
    class Meta:
        model = User
        fields = [
            'user_id',
            'email',
            'first_name',
            'last_name',
            'full_name',  # Added CharField example
            'profile_picture',
            'online_status',
            'last_seen',
            'phone_number',
            'bio'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'profile_picture': {'required': False}
        }

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise ValidationError("A user with this email already exists.")
        return value

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    # Adding SerializerMethodField example
    message_preview = serializers.SerializerMethodField(
        help_text="First 50 characters of message"
    )
    
    class Meta:
        model = Message
        fields = [
            'message_id',
            'sender',
            'message_body',
            'message_preview',  # Added SerializerMethodField
            'sent_at',
            'is_read'
        ]
        read_only_fields = ['sent_at', 'sender']

    def get_message_preview(self, obj):
        return obj.message_body[:50] + '...' if len(obj.message_body) > 50 else obj.message_body

class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)
    # Adding another SerializerMethodField example
    participant_count = serializers.SerializerMethodField(
        help_text="Number of participants in conversation"
    )
    
    class Meta:
        model = Conversation
        fields = [
            'conversation_id',
            'participants',
            'participant_count',  # Added SerializerMethodField
            'created_at',
            'updated_at',
            'messages'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_participant_count(self, obj):
        return obj.participants.count()

    def validate(self, data):
        if 'participants' in data and len(data['participants']) < 2:
            raise ValidationError("A conversation must have at least 2 participants")
        return data

class ConversationCreateSerializer(serializers.ModelSerializer):
    participants = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=User.objects.all(),
        write_only=True
    )
    
    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants']

    def create(self, validated_data):
        try:
            participants = validated_data.pop('participants')
            conversation = Conversation.objects.create(**validated_data)
            conversation.participants.set(participants)
            return conversation
        except DjangoValidationError as e:
            raise ValidationError(str(e))