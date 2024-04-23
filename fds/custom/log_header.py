from django.contrib.auth.signals import user_logged_in
from myapp.models import RequestLog

class RequestLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response


    def __call__(self, request):
        # Print all headers for debugging
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        accept = request.META.get('HTTP_ACCEPT', '')
        accept_encoding = request.META.get('HTTP_ACCEPT_ENCODING', '')
        accept_language = request.META.get('HTTP_ACCEPT_LANGUAGE', '')
        connection = request.META.get('HTTP_CONNECTION', '')
        host = request.META.get('HTTP_HOST', '')
        referer = request.META.get('HTTP_REFERER', '')

        # Custom headers (adjust the keys as needed)
        client_ip = request.META.get('HTTP_X_FORWARDED_FOR', '').split(',')[0].strip()
        if not client_ip:  # Add this check
            client_ip = request.META.get('REMOTE_ADDR', '')

        # Log the request details using the RequestLog model
        if request.method == 'POST':
            request._log_entry = RequestLog(
                user_agent=user_agent,
                client_ip=client_ip,
                accept=accept,
                accept_encoding=accept_encoding,
                accept_language=accept_language,
                connection=connection,
                host=host,
                referer=referer,
                successful_login=False
            )
            request._log_entry.save()

        response = self.get_response(request)
        return response

# Signal handler to update the login status
def update_login_status(sender, request, user, **kwargs):
    if hasattr(request, '_log_entry'):
        request._log_entry.successful_login = True
        request._log_entry.save()

# Connect the signal handler
user_logged_in.connect(update_login_status)
