# Generated by Django 3.2.23 on 2024-04-12 16:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('emr', '0016_auto_20240314_1947'),
    ]

    operations = [
        migrations.RenameField(
            model_name='testresult',
            old_name='test_reults_signed',
            new_name='test_results_signed',
        ),
    ]
