from rest_framework import serializers
from .models import User, Conversation, Message  # Assuming you renamed CustomUser to User

class UserSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'phone_number']


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
    messages = NestedMessageSerializer(many=True, read_only=True)
    latest_message = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'created_at', 'latest_message', 'messages']

    def get_latest_message(self, obj):
        latest = obj.messages.order_by('-sent_at').first()
        return NestedMessageSerializer(latest).data if latest else None


class ConversationCreateSerializer(serializers.ModelSerializer):
    participants = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=User.objects.all()
    )

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants']

    def validate_participants(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("A conversation must include at least two participants.")
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
        if not data['conversation'].participants.filter(id=self.context['request'].user.id).exists():
            raise serializers.ValidationError("You are not a participant in this conversation.")
        return data
