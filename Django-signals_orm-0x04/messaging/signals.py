from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Message,MessageHistory, Notification

@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    """
    Creates a notification for the receiver when a new message is sent
    """
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )

@receiver(pre_save, sender=Message)
def log_message_history(sender, instance, **kwargs):
    """
    Logs previous message content before saving edits
    """
    if instance.pk:  # Only for existing messages (updates)
        try:
            old_message = Message.objects.get(pk=instance.pk)
            if old_message.content != instance.content:  # Only if content changed
                MessageHistory.objects.create(
                    message=instance,
                    content=old_message.content
                )
                instance.edited = True
                instance.edited_at = timezone.now()
        except Message.DoesNotExist:
            pass