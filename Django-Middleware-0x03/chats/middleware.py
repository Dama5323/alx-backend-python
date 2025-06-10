import logging
from datetime import datetime
from django.http import HttpRequest,  HttpResponseForbidden
import time
from django.http import JsonResponse

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
    

class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.message_log = {}  # IP: [(timestamp1), (timestamp2), ...]

    def __call__(self, request):
        # Only track POST requests to the chat endpoint
        if request.method == 'POST' and request.path.startswith('/chats/messages'):
            ip = self.get_client_ip(request)
            now = time.time()
            window = 60  # 60 seconds = 1 minute
            max_requests = 5

            # Clean up old timestamps
            timestamps = self.message_log.get(ip, [])
            timestamps = [ts for ts in timestamps if now - ts < window]
            timestamps.append(now)

            # Check if limit is exceeded
            if len(timestamps) > max_requests:
                return JsonResponse(
                    {"error": "Too many messages sent. Try again in a minute."},
                    status=429
                )

            self.message_log[ip] = timestamps

        return self.get_response(request)

    def get_client_ip(self, request):
        """Get IP address from request headers"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')
    

class RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only apply to protected paths (e.g., sending messages or modifying content)
        protected_paths = ['/chats/messages/', '/chats/admin/']

        if request.path in protected_paths:
            # Assume role is stored in request headers for simplicity (e.g., sent via frontend)
            user_role = request.headers.get('Role', '').lower()

            if user_role not in ['admin', 'moderator']:
                return JsonResponse(
                    {"error": "Forbidden: Insufficient permissions"},
                    status=403
                )

        return self.get_response(request)

