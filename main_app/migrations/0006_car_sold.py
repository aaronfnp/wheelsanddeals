# Generated by Django 4.2.11 on 2024-03-20 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0005_alter_profile_favorite_cars'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='sold',
            field=models.BooleanField(default=False),
        ),
    ]
