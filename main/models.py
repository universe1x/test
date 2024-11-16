from django.db import models
from django.contrib.auth.models import User


class TelegramUser(models.Model):
    telegram_id = models.BigIntegerField(unique=True)
    password = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.telegram_id}"

    class Meta:
        verbose_name = "Telegram User"
        verbose_name_plural = "Telegram Users"

    



