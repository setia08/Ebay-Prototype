# Generated by Django 3.2.15 on 2022-09-23 12:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_auto_20220923_1816'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product_details',
            name='geeks_field',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='userBid', to='auctions.bid'),
        ),
    ]
