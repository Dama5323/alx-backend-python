# chats/middleware.py
import logging
from datetime import datetime

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = logging.getLogger('request')
        self.logger.setLevel(logging.INFO)
        
        # Configure handler only once
        if not self.logger.handlers:
            handler = logging.FileHandler('requests.log')
            handler.setFormatter(logging.Formatter(
                '%(asctime)s - %(message)s'
            ))
            self.logger.addHandler(handler)

    def __call__(self, request):
        response = self.get_response(request)
        
        # Skip logging for certain paths or status codes
        if response.status_code == 404 or request.path.startswith('/static/'):
            return response
            
        user = request.user.username if request.user.is_authenticated else "Anonymous"
        
        self.logger.info(
            f"User: {user} | "
            f"IP: {request.META.get('REMOTE_ADDR')} | " 
            f"Path: {request.path} | "
            f"Method: {request.method} | "
            f"Status: {response.status_code} | "
            f"Size: {len(response.content)} bytes"
)
        
        return response