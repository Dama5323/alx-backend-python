from django.apps import AppConfig

class MessagingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'messaging'  # Must match your directory name exactly

    def ready(self):
        import messaging.signals
