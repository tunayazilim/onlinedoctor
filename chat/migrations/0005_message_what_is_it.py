# Generated by Django 3.2.6 on 2021-10-20 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0004_alter_message_created_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='what_is_it',
            field=models.CharField(default='text', max_length=50, null=True),
        ),
    ]