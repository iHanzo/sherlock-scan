from django.middleware.csrf import get_token
from django.middleware.csrf import CsrfViewMiddleware
import logging

logger = logging.getLogger(__name__)

class RotateCsrfTokenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.method == "POST":
            # Rotate CSRF token
            new_token = get_token(request)
            logger.debug(f"New CSRF token: {new_token}")
        return response