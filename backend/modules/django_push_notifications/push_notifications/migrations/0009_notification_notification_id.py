# Generated by Django 3.2.23 on 2024-05-02 04:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('push_notifications', '0008_rename_type_notification_notification_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='notification_id',
            field=models.CharField(blank=True, max_length=155, null=True),
        ),
    ]