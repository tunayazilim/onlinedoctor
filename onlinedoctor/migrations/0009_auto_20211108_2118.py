# Generated by Django 3.2.6 on 2021-11-08 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onlinedoctor', '0008_indexdoktorlaryazimodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='indexdoktorlaryazimodel',
            name='bottom_title',
            field=models.TextField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='indexdoktorlaryazimodel',
            name='top_title',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
