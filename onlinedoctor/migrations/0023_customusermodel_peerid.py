# Generated by Django 3.2.6 on 2021-12-25 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onlinedoctor', '0022_customusermodel_kimlik'),
    ]

    operations = [
        migrations.AddField(
            model_name='customusermodel',
            name='peerId',
            field=models.CharField(blank=True, default='', max_length=150, null=True),
        ),
    ]