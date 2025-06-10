import logging
from datetime import datetime
from django.http import HttpRequest,  HttpResponseForbidden

logger = logging.getLogger('request_logger')

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        user = "Anonymous"
        if hasattr(request, 'user') and request.user.is_authenticated:
            user = request.user.username
        
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logger.info(log_message)
        
        return self.get_response(request)
    
class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get the current hour (24-hour format)
        current_hour = datetime.now().hour

        # Block access if not between 6PM (18) and 9PM (21)
        if current_hour < 18 or current_hour >= 21:
            return HttpResponseForbidden("Access to the chat is restricted at this time.")

        return self.get_response(request)