from django.db import models
from main.models import TelegramUser

class Resume(models.Model):
    telegram_user = models.ForeignKey(
        TelegramUser, 
        on_delete=models.CASCADE,
        related_name='resumes'
    )
    specialization = models.CharField(max_length=100)
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    city = models.CharField(max_length=50)
    about = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} {self.surname} - {self.specialization}"

    class Meta:
        ordering = ['-created_at']

class Ability(models.Model):
    LEVEL_CHOICES = [
        ('начальный', 'Начальный'),
        ('средний', 'Средний'),
        ('высокий', 'Высокий')
    ]

    resume = models.ForeignKey(Resume, related_name='abilities', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)

    def __str__(self):
        return f"{self.name} ({self.level})"

    class Meta:
        verbose_name_plural = "Abilities"


