from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Message,MessageHistory, Notification
from django.utils import timezone

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
    if instance.pk:  # Only for existing messages
        try:
            old_message = Message.objects.get(pk=instance.pk)
            if old_message.content != instance.content:  # Only if content changed
                MessageHistory.objects.create(
                    message=instance,
                    content=old_message.content,
                    edited_by=old_message.edited_by if hasattr(old_message, 'edited_by') else None
                )
                instance.edited = True
                instance.edited_at = timezone.now()
                # Set the current user as the editor
                from django.contrib.auth import get_user
                user = get_user(instance.sender.request)
                instance.edited_by = user if user.is_authenticated else None
        except Message.DoesNotExist:
            pass
            instance.edited_at = timezone.now()
        except Message.DoesNotExist:
            pass