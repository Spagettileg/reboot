# Generated by Django 3.0.2 on 2020-02-19 17:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_auto_20200205_1222'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='paid',
        ),
    ]
