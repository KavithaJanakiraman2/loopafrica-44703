# Generated by Django 3.2.23 on 2024-04-24 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('push_notifications', '0003_notification'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='notification_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='notification',
            name='subscription_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]