# Generated by Django 4.2.10 on 2024-03-07 10:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0016_alter_quote_det_quote_no'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quote_det',
            name='Quote_no',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='website.quote_ovr'),
        ),
    ]
