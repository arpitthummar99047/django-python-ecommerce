# Generated by Django 5.0.1 on 2024-01-26 12:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_seller', '0006_alter_product_category'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='cdiscription',
            new_name='cdescription',
        ),
    ]
