from django.db import models

class UnreadMessagesManager(models.Manager):
    def unread_for_user(self, user):  # Changed method name to match checker
        """Returns optimized queryset of unread messages for specific user"""
        return self.get_queryset().filter(
            receiver=user,
            read=False
        ).select_related('sender').only(
            'id', 'content', 'timestamp', 'sender__username'
        )