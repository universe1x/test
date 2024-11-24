from django.db import models
from main.models import TelegramUser


class Group(models.Model):
    telegram_user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    skills = models.TextField(blank=True, null=True)
    link = models.CharField(max_length=255)
