# Generated by Django 2.0.3 on 2018-11-11 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0004_auto_20181111_2152'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventory',
            name='item_picture',
            field=models.CharField(max_length=124),
        ),
    ]
