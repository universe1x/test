# Generated by Django 5.1.3 on 2024-11-11 23:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_remove_telegramuser_created_at_telegramuser_password'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='telegramuser',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='telegramuser',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='telegramuser',
            name='user',
        ),
        migrations.RemoveField(
            model_name='telegramuser',
            name='username',
        ),
    ]