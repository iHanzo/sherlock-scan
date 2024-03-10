from django.db import models

class RequestLog(models.Model):
    user_agent = models.TextField()
    client_ip = models.CharField(max_length=100)
    accept = models.TextField()
    accept_encoding = models.TextField()
    accept_language = models.TextField()
    connection = models.TextField()
    host = models.CharField(max_length=100)
    referer = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    successful_login = models.BooleanField(default=False)
    class Meta:
        app_label = 'myapp'
