import logging
from datetime import datetime

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = logging.getLogger('request')
        self.logger.setLevel(logging.INFO)
        handler = logging.FileHandler('requests.log')
        handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
        self.logger.addHandler(handler)

    def __call__(self, request):
        user = request.user.username if request.user.is_authenticated else 'Anonymous'
        self.logger.info(f'User: {user} | Path: {request.path} | Method: {request.method}')
        return self.get_response(request)
