# Generated by Django 5.1.4 on 2024-12-19 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('byt', '0012_delete_laptop'),
    ]

    operations = [
        migrations.CreateModel(
            name='Laptop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.CharField(max_length=100)),
                ('product', models.CharField(max_length=100)),
                ('type_name', models.CharField(max_length=100)),
                ('inches', models.FloatField()),
                ('ram', models.IntegerField()),
                ('operating_system', models.CharField(max_length=100)),
                ('weight', models.FloatField()),
                ('price_euros', models.FloatField()),
                ('screen_type', models.CharField(max_length=100)),
                ('screen_width', models.IntegerField()),
                ('screen_height', models.IntegerField()),
                ('touchscreen', models.BooleanField()),
                ('ips_panel', models.BooleanField()),
                ('retina_display', models.BooleanField()),
                ('cpu_company', models.CharField(max_length=100)),
                ('cpu_frequency', models.FloatField()),
                ('cpu_model', models.CharField(max_length=100)),
                ('primary_storage_capacity', models.CharField(max_length=100)),
                ('secondary_storage_capacity', models.CharField(blank=True, max_length=100, null=True)),
                ('primary_storage_type', models.CharField(max_length=100)),
                ('secondary_storage_type', models.CharField(blank=True, max_length=100, null=True)),
                ('gpu_company', models.CharField(max_length=100)),
                ('gpu_model', models.CharField(max_length=100)),
                ('gpu_full_model', models.CharField(max_length=100)),
                ('year', models.IntegerField()),
                ('quarter', models.CharField(max_length=10)),
                ('architecture', models.CharField(max_length=100)),
                ('process_nm', models.IntegerField()),
                ('cores_shaders', models.CharField(max_length=100)),
                ('base_clock_mhz', models.CharField(max_length=100)),
                ('memory_size_gb', models.CharField(max_length=100)),
                ('memory_type', models.CharField(blank=True, max_length=100, null=True)),
                ('memory_bus_width_bits', models.CharField(blank=True, max_length=100, null=True)),
                ('tdp_w', models.CharField(blank=True, max_length=100, null=True)),
                ('integrated_gpu', models.BooleanField()),
                ('mobile_gpu', models.BooleanField()),
                ('quantity', models.IntegerField()),
            ],
        ),
    ]
