# Generated by Django 3.2.6 on 2022-03-07 16:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0012_room_totaldurationtime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='totalDurationTime',
            field=models.DateTimeField(blank=True, default=datetime.datetime(1, 1, 1, 0, 0), null=True),
        ),
    ]
