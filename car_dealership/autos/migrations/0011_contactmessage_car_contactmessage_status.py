# Generated by Django 5.1.7 on 2025-04-10 06:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autos', '0010_car_featured_car_featured_image_car_image_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactmessage',
            name='car',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='autos.car'),
        ),
        migrations.AddField(
            model_name='contactmessage',
            name='status',
            field=models.CharField(choices=[('pending', 'Pendiente'), ('contacted', 'Contactado'), ('resolved', 'Resuelto')], default='pending', max_length=20),
        ),
    ]
