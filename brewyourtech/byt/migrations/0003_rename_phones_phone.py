# Generated by Django 5.1.4 on 2024-12-18 20:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('byt', '0002_phones'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Phones',
            new_name='Phone',
        ),
    ]
