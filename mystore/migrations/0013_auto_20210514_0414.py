# Generated by Django 3.2.2 on 2021-05-14 01:14

from django.db import migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('mystore', '0012_rename_country_billingaddress_countries'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='billingaddress',
            name='countries',
        ),
        migrations.AddField(
            model_name='billingaddress',
            name='country',
            field=django_countries.fields.CountryField(default='Egypt', max_length=10),
            preserve_default=False,
        ),
    ]
