# Generated by Django 5.0.3 on 2024-03-20 14:32

import django.core.validators
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0010_alter_car_previous_owners'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='date_listed',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='car',
            name='price',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(999999)]),
        ),
    ]