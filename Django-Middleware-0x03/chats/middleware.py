import logging
from django.utils import timezone
from django.http import HttpResponseForbidden
from datetime import time
from django.conf import settings

logger = logging.getLogger('request_logger')


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        timestamp = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
        user = request.user.username if request.user.is_authenticated else 'Anonymous'
        path = request.path

        logger.info(f"{timestamp} - User: {user} - Path: {path}")
        
        return self.get_response(request)
    

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.allowed_start = time(18, 0)  # 6 PM
        self.allowed_end = time(21, 0)    # 9 PM

    def __call__(self, request):
        # Apply only to /messaging/ path
        if request.path.startswith('/messaging/'):
            current_time = timezone.localtime().time()

            if not (self.allowed_start <= current_time <= self.allowed_end):
                return HttpResponseForbidden(
                    "Access to the messaging app is only allowed between 6PM and 9PM."
                )
        
        return self.get_response(request)
