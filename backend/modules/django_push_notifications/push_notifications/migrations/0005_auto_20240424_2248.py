# Generated by Django 3.2.23 on 2024-04-24 17:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('push_notifications', '0004_auto_20240424_2019'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='notification_id',
        ),
        migrations.RemoveField(
            model_name='notification',
            name='subscription_id',
        ),
    ]
