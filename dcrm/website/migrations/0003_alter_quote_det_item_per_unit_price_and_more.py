# Generated by Django 4.2.10 on 2024-04-17 16:48

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_quote_det_quote_ovr_delete_record_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quote_det',
            name='Item_per_unit_price',
            field=models.PositiveIntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='quote_ovr',
            name='Phone',
            field=models.CharField(max_length=15, null=True, validators=[django.core.validators.RegexValidator('^[1-9]\\d*$')]),
        ),
    ]
