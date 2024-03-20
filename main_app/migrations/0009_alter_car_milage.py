# Generated by Django 5.0.3 on 2024-03-20 14:21

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0008_alter_car_milage_alter_car_previous_owners_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='milage',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(999999)]),
        ),
    ]