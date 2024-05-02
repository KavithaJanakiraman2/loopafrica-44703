# Generated by Django 3.2.23 on 2024-04-30 10:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0028_auto_20240430_1500'),
    ]

    operations = [
        migrations.RenameField(
            model_name='appointment',
            old_name='join_url',
            new_name='application_type',
        ),
        migrations.RemoveField(
            model_name='appointment',
            name='meeting_id',
        ),
        migrations.RemoveField(
            model_name='appointment',
            name='password',
        ),
        migrations.CreateModel(
            name='Zoom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meeting_id', models.CharField(blank=True, max_length=255, null=True)),
                ('join_url', models.CharField(blank=True, max_length=255, null=True)),
                ('password', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('appointment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='zoom_appointment', to='users.appointment')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='zoom_created_by', to=settings.AUTH_USER_MODEL)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='zoom_doctor', to='users.doctor')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='zoom_updated_by', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='zoom_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
