# Generated by Django 2.2 on 2020-01-22 16:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('donation', '0033_auto_20200122_1108'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='challengescomments',
            name='user_profile',
        ),
        migrations.AddField(
            model_name='challengescomments',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='comment_user', to=settings.AUTH_USER_MODEL),
        ),
    ]