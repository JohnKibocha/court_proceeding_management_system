# Generated by Django 5.0.2 on 2024-03-18 14:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('court_proceedings_management_application', '0005_relief_case'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='relief',
            name='case',
        ),
    ]
