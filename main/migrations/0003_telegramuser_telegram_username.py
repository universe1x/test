# Generated by Django 5.1.3 on 2024-11-26 05:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_telegramuser_telegram_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='telegramuser',
            name='telegram_username',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
