# Generated by Django 2.2 on 2020-01-07 20:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donation', '0002_challenges_donatorapproved'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profilePhoto',
            field=models.FileField(default='default-ava.jpg', upload_to=''),
        ),
    ]