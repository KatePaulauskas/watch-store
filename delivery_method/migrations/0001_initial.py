# Generated by Django 5.1 on 2024-08-31 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DeliveryMethod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('description', models.TextField(blank=True)),
                ('weight_min', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('weight_max', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('cost', models.DecimalField(decimal_places=2, max_digits=6)),
            ],
        ),
    ]
