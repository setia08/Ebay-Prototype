# Generated by Django 3.2.15 on 2022-09-24 05:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0010_product_details_owner'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bid',
            old_name='bid',
            new_name='bid_amount',
        ),
    ]
