from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class TelegramUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='telegram_profile')
    telegram_id = models.BigIntegerField(unique=True)
    username = models.CharField(max_length=100, blank=True, null=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.telegram_id}"

class TelegramAuthToken(models.Model):
    token = models.CharField(max_length=100, unique=True)
    telegram_id = models.BigIntegerField()
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    expires_at = models.DateTimeField()
    
    def __str__(self):
        return f"Token for {self.telegram_id}"
    
    def is_expired(self):
        return timezone.now() > self.expires_at


