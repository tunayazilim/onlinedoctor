# Generated by Django 3.2.6 on 2021-11-19 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onlinedoctor', '0018_remove_footermodel_footerlogo'),
    ]

    operations = [
        migrations.AddField(
            model_name='timeschedulemodel',
            name='status',
            field=models.CharField(default='pending', max_length=100),
        ),
    ]