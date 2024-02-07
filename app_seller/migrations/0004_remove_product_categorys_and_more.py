# Generated by Django 5.0.1 on 2024-01-26 11:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_seller', '0003_product_sub_categorys'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='categorys',
        ),
        migrations.RemoveField(
            model_name='product',
            name='sub_categorys',
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cname', models.CharField(max_length=200)),
                ('cdiscription', models.TextField(max_length=200)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_seller.seller')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='categlory',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app_seller.category'),
        ),
    ]
