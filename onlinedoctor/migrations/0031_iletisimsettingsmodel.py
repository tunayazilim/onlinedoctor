# Generated by Django 3.2.6 on 2022-02-26 16:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('onlinedoctor', '0030_remove_customusermodel_peerid'),
    ]

    operations = [
        migrations.CreateModel(
            name='iletisimSettingsModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('whatsapp', models.CharField(blank=True, max_length=250, null=True)),
                ('zoom', models.CharField(blank=True, max_length=250, null=True)),
                ('skype', models.CharField(blank=True, max_length=250, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='iletisimSettings', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'iletisim_ayarlar_',
                'verbose_name_plural': 'iletisim_ayarlari_',
                'db_table': 'iletisimSettingsModel',
            },
        ),
    ]