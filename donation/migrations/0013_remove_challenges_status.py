# Generated by Django 2.2 on 2020-01-08 18:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('donation', '0012_auto_20200108_1313'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='challenges',
            name='status',
        ),
    ]
