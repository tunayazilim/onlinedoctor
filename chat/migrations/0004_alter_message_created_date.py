# Generated by Django 3.2.6 on 2021-10-18 22:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_auto_20211014_1728'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='created_date',
            field=models.TimeField(auto_now_add=True),
        ),
    ]
