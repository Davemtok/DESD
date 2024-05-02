# Generated by Django 4.1.4 on 2024-05-02 03:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0006_appointment_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='is_surgery',
            field=models.BooleanField(default=False, help_text='True if the appointment is for a surgery.'),
        ),
    ]
