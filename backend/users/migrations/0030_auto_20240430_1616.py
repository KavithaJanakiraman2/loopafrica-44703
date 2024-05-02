# Generated by Django 3.2.23 on 2024-04-30 10:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0029_auto_20240430_1547'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='zoom',
            name='doctor',
        ),
        migrations.RemoveField(
            model_name='zoom',
            name='user',
        ),
        migrations.AlterField(
            model_name='zoom',
            name='appointment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='zoom_appointment', to='users.appointment'),
        ),
    ]