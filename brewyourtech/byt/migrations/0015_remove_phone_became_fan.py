# Generated by Django 5.1.4 on 2024-12-31 07:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('byt', '0014_bookmark'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='phone',
            name='became_fan',
        ),
    ]