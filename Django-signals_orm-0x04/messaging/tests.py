from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Message, Notification

User = get_user_model()

class MessagingTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='testpass123')
        self.user2 = User.objects.create_user(username='user2', password='testpass123')
    
    def test_message_creation(self):
        message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content="Hello there!"
        )
        self.assertEqual(Message.objects.count(), 1)
        self.assertEqual(message.sender, self.user1)
        self.assertEqual(message.receiver, self.user2)
    
    def test_notification_creation_signal(self):
        # Verify notification is created automatically via signal
        message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content="Test notification"
        )
        self.assertEqual(Notification.objects.count(), 1)
        notification = Notification.objects.first()
        self.assertEqual(notification.user, self.user2)
        self.assertEqual(notification.message, message)
        self.assertFalse(notification.is_read)
    
    def test_notification_str_representation(self):
        message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content="Test message"
        )
        notification = Notification.objects.create(
            user=self.user2,
            message=message,
            is_read=False
        )
        self.assertEqual(
            str(notification),
            f"Notification for {self.user2} about message #{message.id}"
        )