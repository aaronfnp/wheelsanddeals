# Generated by Django 5.0.3 on 2024-03-20 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0007_alter_car_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='milage',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='car',
            name='previous_owners',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='car',
            name='price',
            field=models.FloatField(),
        ),
    ]
