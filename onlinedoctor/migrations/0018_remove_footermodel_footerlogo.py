# Generated by Django 3.2.6 on 2021-11-19 13:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('onlinedoctor', '0017_logomodel'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='footermodel',
            name='footerLogo',
        ),
    ]
