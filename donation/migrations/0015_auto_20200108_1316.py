# Generated by Django 2.2 on 2020-01-08 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donation', '0014_challenges_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='challenges',
            name='status',
            field=models.CharField(default='Active', max_length=20),
        ),
    ]