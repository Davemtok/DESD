# Generated by Django 4.1.4 on 2024-05-01 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_user_is_admin'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='location',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='postcode',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
    ]
