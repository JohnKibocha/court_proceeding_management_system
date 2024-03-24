# Generated by Django 5.0.2 on 2024-03-19 10:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('court_proceedings_management_application', '0010_invoice_participant'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='relieved_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='court_proceedings_management_application.relief'),
        ),
    ]