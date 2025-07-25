from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from .managers import UnreadMessagesManage

User = get_user_model()

class UnreadMessagesManager(models.Manager):
    pass

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    parent_message = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    edited = models.BooleanField(default=False)
    edited_at = models.DateTimeField(null=True, blank=True)
    edited_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='edited_messages')

    # Managers
    objects = models.Manager()  # Default manager
    unread = UnreadMessagesManager()  # Custom manager 
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['parent_message']),
        ]

    
    def __str__(self):
        return f"Message from {self.sender} to {self.receiver}"
    
    def mark_as_read(self):
        """Helper method to mark a message as read"""
        self.read = True
        self.save(update_fields=['read'])
    
    @property
    def is_reply(self):
        return self.parent_message is not None
    
    def get_thread(self):
        """Returns the root message of the thread"""
        return self.parent_message.get_thread() if self.is_reply else self
    
    
class MessageHistory(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='history')
    content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)
    edited_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    class Meta:
        ordering = ['-edited_at']
        verbose_name_plural = 'Message Histories'
    
    def __str__(self):
        return f"History for message #{self.message.id} at {self.edited_at}"

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Notification for {self.user} about message #{self.message.id}"
    
class UnreadMessagesManager(models.Manager):
    def for_user(self, user):
        """Returns unread messages for a specific user"""
        return self.get_queryset().filter(
            receiver=user,
            read=False
        ).select_related('sender').only(
            'id', 'content', 'timestamp', 'sender__username'
        )
    