# Generated by Django 5.1.7 on 2025-04-11 00:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_notification_alter_jante_dernier_ndi_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='is_read',
            field=models.BooleanField(default=False),
        ),
    ]
