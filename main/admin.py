from django.contrib import admin
from .models import TelegramUser, TelegramAuthToken

admin.site.register(TelegramUser)
admin.site.register(TelegramAuthToken)
# Register your models here.
