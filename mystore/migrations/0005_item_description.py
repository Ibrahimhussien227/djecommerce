# Generated by Django 3.2.2 on 2021-05-11 21:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mystore', '0004_item_discount_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='description',
            field=models.TextField(default='asdas'),
            preserve_default=False,
        ),
    ]
