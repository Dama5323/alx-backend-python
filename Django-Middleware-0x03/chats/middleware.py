import logging
from django.utils import timezone
from django.http import HttpResponseForbidden
from datetime import time
from django.conf import settings

logger = logging.getLogger('request_logger')
from collections import defaultdict, deque
from django.http import JsonResponse


from datetime import datetime
from datetime import datetime

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        user = "Anonymous"
        if hasattr(request, 'user') and request.user.is_authenticated:
            user = request.user.username  # or request.user.email if you prefer
        
        log_entry = f"{datetime.now()} - User: {user} - Path: {request.path}\n"
        
        with open('requests.log', 'a') as log_file:
            log_file.write(log_entry)
        
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
    
    class RequestLoggingMiddleware:
        def __init__(self, get_response):
            self.get_response = get_response
            self.ip_message_times = defaultdict(deque)
            self.message_limit = 5
            self.time_window = 60  # seconds (1 minute)

    def __call__(self, request):
        if request.method == "POST" and request.path.startswith('/chat/'):
            ip = self.get_client_ip(request)
            now = time.time()
            timestamps = self.ip_message_times[ip]

            # Remove timestamps older than the time window
            while timestamps and now - timestamps[0] > self.time_window:
                timestamps.popleft()

            if len(timestamps) >= self.message_limit:
                # Block request - limit exceeded
                return JsonResponse({
                    "error": "Message limit exceeded. Only 5 messages per minute allowed."
                }, status=429)  # 429 Too Many Requests

            # Add current request timestamp
            timestamps.append(now)

        return self.get_response(request)

    def get_client_ip(self, request):
        """Extract IP address from request."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    

class RolePermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        return response
    
    def process_view(self, request, view_func, view_args, view_kwargs):
        # Skip permission checks for admin URLs
        if request.path.startswith('/admin/'):
            return None
        
        # Your existing permission logic here
        required_roles = getattr(view_func, 'required_roles', [])
        if required_roles:
            if not request.user.is_authenticated:
                return HttpResponseForbidden("Authentication required")
            
            user_roles = getattr(request.user, 'roles', [])
            if not any(role in required_roles for role in user_roles):
                return HttpResponseForbidden("Insufficient permissions")
        
        return None