# Generated by Django 4.2.10 on 2024-03-30 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0003_quote_ovr_visible'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quote_det',
            name='Item_per_unit_price',
            field=models.PositiveIntegerField(default=0, null=True),
        ),
    ]