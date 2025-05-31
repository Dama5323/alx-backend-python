# chats/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator

class User(AbstractUser):
    # Personal Info
    profile_picture = models.ImageField(
        upload_to='profile_pics/',
        null=True,
        blank=True,
        help_text="User's profile picture"
    )
    bio = models.TextField(
        blank=True,
        null=True,
        max_length=500,
        help_text="Short bio about the user"
    )
    
    # Contact Information
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be in format: '+999999999'. Up to 15 digits allowed."
    )
    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=17,
        blank=True,
        null=True,
        help_text="Contact phone number"
    )
    
    # Status Information
    online_status = models.BooleanField(
        default=False,
        help_text="Whether the user is currently online"
    )
    last_seen = models.DateTimeField(
        auto_now=True,
        help_text="Last time the user was active"
    )
    
    # Override default fields to make them required
    first_name = models.CharField(
        max_length=150,
        blank=False,
        help_text="User's first name"
    )
    last_name = models.CharField(
        max_length=150,
        blank=False,
        help_text="User's last name"
    )
    email = models.EmailField(
        blank=False,
        unique=True,
        help_text="User's email address"
    )
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.username})"

class Conversation(models.Model):
    participants = models.ManyToManyField(
        User,
        related_name='conversations',
        help_text="Users participating in this conversation"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When the conversation was started"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Last activity in the conversation"
    )
    
    class Meta:
        ordering = ['-updated_at']
        verbose_name = "Conversation"
        verbose_name_plural = "Conversations"

    def __str__(self):
        participant_names = ", ".join([user.username for user in self.participants.all()])
        return f"Conversation between {participant_names} (last updated: {self.updated_at})"

class Message(models.Model):
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_messages',
        help_text="User who sent the message"
    )
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages',
        help_text="Conversation this message belongs to"
    )
    content = models.TextField(
        help_text="The message content"
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
        help_text="When the message was sent"
    )
    is_read = models.BooleanField(
        default=False,
        help_text="Whether the message has been read by recipients"
    )
    
    class Meta:
        ordering = ['timestamp']
        verbose_name = "Message"
        verbose_name_plural = "Messages"

    def __str__(self):
        return f"From {self.sender.username} at {self.timestamp.strftime('%Y-%m-%d %H:%M')}: {self.content[:50]}..."