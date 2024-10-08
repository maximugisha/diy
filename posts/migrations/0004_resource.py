# Generated by Django 4.2.16 on 2024-09-26 22:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import djrichtextfield.models
import posts.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0003_remove_post_images_post_images'),
    ]

    operations = [
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=255)),
                ('type', models.CharField(choices=[('video', 'Video'), ('image', 'Image'), ('pdf', 'PDF'), ('document', 'Document'), ('zip', 'Zip')], default='pdf', max_length=20)),
                ('content', djrichtextfield.models.RichTextField()),
                ('attachment', models.FileField(upload_to='attachments', validators=[posts.models.validate_file_extension, posts.models.validate_file_size])),
                ('audience', models.CharField(choices=[('public', 'Public'), ('organization', 'My Organization'), ('draft', 'Draft')], default='public', max_length=20)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resource_author', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['id'],
                'abstract': False,
            },
        ),
    ]
