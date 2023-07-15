from django.db import models


class ZohoToken(models.Model):
    access_token = models.TextField()
    refresh_token = models.TextField()
    timestamp = models.DateTimeField(auto_now=True)
