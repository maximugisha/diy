# Generated by Django 4.2.16 on 2024-10-14 11:59

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_session_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='start_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
