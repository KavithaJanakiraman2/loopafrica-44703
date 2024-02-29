# Generated by Django 3.2.23 on 2024-02-29 14:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_patientinfo_genotype'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vitals',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('heart_rate', models.IntegerField()),
                ('blood_status', models.CharField(max_length=100)),
                ('blood_count', models.IntegerField()),
                ('glucose_level', models.DecimalField(decimal_places=2, max_digits=10)),
                ('weight', models.DecimalField(decimal_places=2, max_digits=10)),
                ('temperature', models.DecimalField(decimal_places=2, max_digits=5)),
                ('pulse', models.IntegerField()),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('last_updated_at', models.DateTimeField(blank=True, null=True)),
                ('last_updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vitals_last_updated_by', to=settings.AUTH_USER_MODEL)),
                ('patient_info', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.patientinfo')),
            ],
        ),
    ]
