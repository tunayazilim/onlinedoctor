# Generated by Django 3.2.6 on 2022-03-07 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0011_alter_room_appoitmentdayandtime'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='totalDurationTime',
            field=models.PositiveSmallIntegerField(blank=True, default=0, null=True),
        ),
    ]
