# Generated by Django 5.1.4 on 2024-12-19 05:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('byt', '0008_tablet'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tablet',
            name='battery_capacity',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='tablet',
            name='memory_card_upto',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='tablet',
            name='memory_inbuilt',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='tablet',
            name='price',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='tablet',
            name='ram',
            field=models.CharField(max_length=100),
        ),
    ]
