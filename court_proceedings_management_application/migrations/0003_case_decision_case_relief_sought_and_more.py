# Generated by Django 5.0.2 on 2024-03-16 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('court_proceedings_management_application', '0002_alter_court_court_logo'),
    ]

    operations = [
        migrations.AddField(
            model_name='case',
            name='decision',
            field=models.TextField(blank=True, choices=[('dismissed', 'Dismissed'), ('upheld', 'Upheld'), ('overturned', 'Overturned'), ('compensated', 'Compensated'), ('acquitted', 'Acquitted'), ('convicted', 'Convicted'), ('sentenced', 'Sentenced'), ('fined', 'Fined'), ('imprisoned', 'Imprisoned'), ('community service', 'Community Service'), ('probation', 'Probation'), ('parole', 'Parole'), ('suspended sentence', 'Suspended Sentence'), ('death penalty', 'Death Penalty'), ('life imprisonment', 'Life Imprisonment'), ('acquitted', 'Acquitted'), ('discharged', 'Discharged'), ('reprimanded', 'Reprimanded'), ('warned', 'Warned'), ('rehabilitated', 'Rehabilitated'), ('restitution', 'Restitution'), ('compensation', 'Compensation'), ('damages', 'Damages'), ('injunction', 'Injunction'), ('restraining order', 'Restraining Order'), ('restitution', 'Restitution'), ('reparations', 'Reparations')], null=True),
        ),
        migrations.AddField(
            model_name='case',
            name='relief_sought',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='caseproceeding',
            name='custodial_sentence',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='caseproceeding',
            name='monetary_relief',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='caseproceeding',
            name='verdict',
            field=models.CharField(blank=True, choices=[('dismissed', 'Dismissed'), ('upheld', 'Upheld'), ('overturned', 'Overturned'), ('compensated', 'Compensated'), ('acquitted', 'Acquitted'), ('convicted', 'Convicted'), ('sentenced', 'Sentenced'), ('fined', 'Fined'), ('imprisoned', 'Imprisoned'), ('community service', 'Community Service'), ('probation', 'Probation'), ('parole', 'Parole'), ('suspended sentence', 'Suspended Sentence'), ('death penalty', 'Death Penalty'), ('life imprisonment', 'Life Imprisonment'), ('acquitted', 'Acquitted'), ('discharged', 'Discharged'), ('reprimanded', 'Reprimanded'), ('warned', 'Warned'), ('rehabilitated', 'Rehabilitated'), ('restitution', 'Restitution'), ('compensation', 'Compensation'), ('damages', 'Damages'), ('injunction', 'Injunction'), ('restraining order', 'Restraining Order'), ('restitution', 'Restitution'), ('reparations', 'Reparations')], max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='case',
            name='case_description',
            field=models.TextField(blank=True, null=True),
        ),
    ]