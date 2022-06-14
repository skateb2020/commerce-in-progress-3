# Generated by Django 3.2.5 on 2022-05-22 23:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0015_remove_listings_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='listings',
            name='user',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]