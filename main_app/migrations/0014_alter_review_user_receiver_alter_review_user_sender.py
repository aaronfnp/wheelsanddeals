# Generated by Django 4.2.11 on 2024-03-21 17:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main_app', '0013_merge_20240321_1429'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='user_receiver',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='received_reviews', to='main_app.profile'),
        ),
        migrations.AlterField(
            model_name='review',
            name='user_sender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_reviews', to=settings.AUTH_USER_MODEL),
        ),
    ]
