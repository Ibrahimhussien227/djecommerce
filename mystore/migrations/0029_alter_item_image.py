# Generated by Django 3.2.2 on 2021-05-16 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mystore', '0028_alter_item_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
