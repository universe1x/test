# Generated by Django 5.1.3 on 2024-11-27 08:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_telegramuser_telegram_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='telegramuser',
            name='telegram_username',
        ),
    ]