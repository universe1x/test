# Generated by Django 5.1.3 on 2024-11-27 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0004_alter_group_specialization'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='specialization',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]