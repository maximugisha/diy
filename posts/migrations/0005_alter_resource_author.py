# Generated by Django 4.2.16 on 2024-09-26 22:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0004_resource'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resource',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
