# Generated by Django 3.2.6 on 2021-11-05 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onlinedoctor', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timeschedulemodel',
            name='date',
            field=models.DateField(null=True),
        ),
    ]