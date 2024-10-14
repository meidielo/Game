# Generated by Django 5.1.1 on 2024-10-13 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0003_rename_name_profile_username_profile_points_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='user',
        ),
        migrations.AddField(
            model_name='profile',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True, verbose_name='last login'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='confirm_password',
            field=models.CharField(default='defaultpassword', max_length=255),
        ),
        migrations.AlterField(
            model_name='profile',
            name='password',
            field=models.CharField(default='defaultpassword', max_length=255),
        ),
        migrations.AlterField(
            model_name='profile',
            name='username',
            field=models.CharField(default='defaultusername', max_length=255, unique=True),
        ),
    ]
