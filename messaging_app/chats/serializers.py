from rest_framework import serializers
from .models import CustomUser, Conversation, Message
from rest_framework.exceptions import ValidationError  # This is the correct import

class UserSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(required=False)

    class Meta:
        model = CustomUser
        fields = ['user_id', 'email', 'first_name', 'last_name', 'phone_number']

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['message_id', 'conversation', 'sender', 'message_body', 'sent_at']
        read_only_fields = ['sender', 'sent_at']

class NestedMessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'message_body', 'sent_at']

class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = NestedMessageSerializer(many=True, read_only=True, source='message_set')
    latest_message = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'created_at', 'latest_message', 'messages']

    def get_latest_message(self, obj):
        latest = obj.message_set.order_by('-sent_at').first()
        return NestedMessageSerializer(latest).data if latest else None

class ConversationCreateSerializer(serializers.ModelSerializer):
    participants = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=CustomUser.objects.all()
    )

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants']

    def validate_participants(self, value):
        if len(value) < 2:
            raise ValidationError("A conversation must include at least two participants.")
        return value

    def create(self, validated_data):
        participants = validated_data.pop('participants')
        conversation = Conversation.objects.create(**validated_data)
        conversation.participants.set(participants)
        return conversation

class MessageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['message_id', 'conversation', 'message_body']
        
    def validate(self, data):
        if not data['conversation'].participants.filter(user_id=self.context['request'].user.user_id).exists():
            raise ValidationError("You are not a participant in this conversation.")
        return data