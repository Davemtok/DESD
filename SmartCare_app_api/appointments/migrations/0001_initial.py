# Generated by Django 4.1.4 on 2024-03-27 20:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('appointment_date', models.DateField()),
                ('appointment_time', models.TimeField()),
                ('status', models.CharField(choices=[('scheduled', 'Scheduled'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='scheduled', max_length=10)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointments_as_patient', to=settings.AUTH_USER_MODEL)),
                ('provider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointments_as_provider', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]