# Generated by Django 5.0.2 on 2024-03-18 14:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('court_proceedings_management_application', '0004_remove_caseproceeding_custodial_sentence_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='relief',
            name='case',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='court_proceedings_management_application.case'),
        ),
    ]