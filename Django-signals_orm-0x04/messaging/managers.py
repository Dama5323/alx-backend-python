from django.db import models

class UnreadMessagesManager(models.Manager):
    def for_user(self, user):
        """Returns unread messages optimized for inbox display"""
        return self.get_queryset().filter(
            receiver=user,
            read=False
        ).select_related('sender').only(
            'id', 'content', 'timestamp', 'sender__username'
        )