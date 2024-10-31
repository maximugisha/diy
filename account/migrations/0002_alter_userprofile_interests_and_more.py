# Generated by Django 4.2.16 on 2024-09-23 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='interests',
            field=models.ManyToManyField(blank=True, null=True, related_name='interests', to='account.interest'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='profile_picture',
            field=models.ImageField(blank=True, default='no_profile_Pic.jpeg', null=True, upload_to='profile_pics'),
        ),
    ]
