# Generated by Django 3.2.2 on 2021-05-22 20:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mystore', '0032_auto_20210522_2302'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='label',
            field=models.CharField(choices=[('P', 'primary'), ('S', 'secondary'), ('D', 'danger')], max_length=10),
        ),
    ]
