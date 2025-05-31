# chats/serializers.py
from rest_framework import serializers
from .models import User, Conversation, Message

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'user_id',
            'email',
            'first_name',
            'last_name',
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

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone_number=validated_data.get('phone_number'),
            bio=validated_data.get('bio')
        )
        return user

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    
    class Meta:
        model = Message
        fields = [
            'message_id',
            'sender',
            'message_body',
            'sent_at',
            'is_read'
        ]
        read_only_fields = ['sent_at', 'sender']

class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Conversation
        fields = [
            'conversation_id',
            'participants',
            'created_at',
            'updated_at',
            'messages'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def create(self, validated_data):
        participants_data = validated_data.pop('participants', [])
        conversation = Conversation.objects.create(**validated_data)
        conversation.participants.set(participants_data)
        return conversation

class ConversationCreateSerializer(serializers.ModelSerializer):
    participants = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=User.objects.all(),
        write_only=True
    )
    
    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants']