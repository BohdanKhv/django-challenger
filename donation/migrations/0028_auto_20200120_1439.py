# Generated by Django 2.2 on 2020-01-20 19:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('donation', '0027_auto_20200118_1203'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='challenges',
            options={'ordering': ['-published'], 'verbose_name_plural': 'Challenges'},
        ),
        migrations.CreateModel(
            name='ChallengesComments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('about', models.TextField(max_length=500)),
                ('published', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('challenge', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='comment_challenge', to='donation.Challenges')),
                ('user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='comment_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Challenges Comments',
                'ordering': ['-published'],
            },
        ),
    ]