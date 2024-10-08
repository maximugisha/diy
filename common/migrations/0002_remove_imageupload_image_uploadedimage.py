# Generated by Django 4.2.16 on 2024-09-26 12:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='imageupload',
            name='image',
        ),
        migrations.CreateModel(
            name='UploadedImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='uploads/')),
                ('image_upload', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='common.imageupload')),
            ],
        ),
    ]
