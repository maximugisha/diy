# Generated by Django 4.2.16 on 2024-09-26 12:57

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_remove_post_images_post_images'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='images',
        ),
        migrations.AddField(
            model_name='post',
            name='images',
            field=models.UUIDField(default=uuid.uuid4),
        ),
    ]
