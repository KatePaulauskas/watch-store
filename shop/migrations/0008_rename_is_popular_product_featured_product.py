# Generated by Django 5.1 on 2024-09-09 11:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_product_is_popular'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='is_popular',
            new_name='featured_product',
        ),
    ]
