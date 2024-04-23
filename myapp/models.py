from django.db import models

class RequestLog(models.Model):
    user_agent = models.TextField()
    accept = models.TextField()
    accept_encoding = models.TextField()
    accept_language = models.TextField()
    connection = models.TextField()
    host = models.CharField(max_length=100)
    client_ip = models.CharField(max_length=100, blank=True, null=True)
    referer = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    successful_login = models.BooleanField(default=False)