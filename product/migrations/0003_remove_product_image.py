# Generated by Django 5.0 on 2023-12-10 17:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_productimage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='image',
        ),
    ]
