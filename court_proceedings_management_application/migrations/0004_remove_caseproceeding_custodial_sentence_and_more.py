# Generated by Django 5.0.2 on 2024-03-18 13:20

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('court_proceedings_management_application', '0003_case_decision_case_relief_sought_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='caseproceeding',
            name='custodial_sentence',
        ),
        migrations.RemoveField(
            model_name='caseproceeding',
            name='monetary_relief',
        ),
        migrations.RemoveField(
            model_name='caseproceeding',
            name='verdict',
        ),
        migrations.CreateModel(
            name='Relief',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('relief_type', models.CharField(choices=[('monetary', 'Monetary'), ('custodial', 'Custodial')], max_length=10)),
                ('verdict', models.CharField(choices=[('dismissed', 'Dismissed'), ('upheld', 'Upheld'), ('overturned', 'Overturned'), ('compensated', 'Compensated'), ('acquitted', 'Acquitted'), ('convicted', 'Convicted'), ('sentenced', 'Sentenced'), ('fined', 'Fined'), ('imprisoned', 'Imprisoned'), ('community service', 'Community Service'), ('probation', 'Probation'), ('parole', 'Parole'), ('suspended sentence', 'Suspended Sentence'), ('death penalty', 'Death Penalty'), ('life imprisonment', 'Life Imprisonment'), ('acquitted', 'Acquitted'), ('discharged', 'Discharged'), ('reprimanded', 'Reprimanded'), ('warned', 'Warned'), ('rehabilitated', 'Rehabilitated'), ('restitution', 'Restitution'), ('compensation', 'Compensation'), ('damages', 'Damages'), ('injunction', 'Injunction'), ('restraining order', 'Restraining Order'), ('restitution', 'Restitution'), ('reparations', 'Reparations')], max_length=255)),
                ('value', models.IntegerField()),
                ('court', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='court_proceedings_management_application.court')),
                ('participant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='caseproceeding',
            name='reliefs',
            field=models.ManyToManyField(blank=True, to='court_proceedings_management_application.relief'),
        ),
    ]
