# Generated by Django 5.0.1 on 2024-01-17 03:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_buyer', '0004_alter_user_profile_pic'),
    ]

    operations = [
        migrations.CreateModel(
            name='Orderdetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=200)),
                ('last_name', models.CharField(max_length=200)),
                ('search_country', models.CharField(max_length=200)),
                ('order_address_line1', models.CharField(max_length=200)),
                ('order_address_line2', models.CharField(max_length=200)),
                ('order_city', models.CharField(max_length=200)),
                ('order_zipcode', models.CharField(max_length=200)),
                ('order_phone', models.CharField(max_length=200)),
            ],
        ),
    ]
