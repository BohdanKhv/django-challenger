# Generated by Django 2.2 on 2020-01-08 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donation', '0016_remove_challenges_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='challenges',
            name='status',
            field=models.CharField(default='Active', max_length=20),
        ),
    ]
