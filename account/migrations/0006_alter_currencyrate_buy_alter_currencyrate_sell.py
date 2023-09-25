# Generated by Django 4.2.3 on 2023-07-06 16:11

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("account", "0005_alter_atm_options"),
    ]

    operations = [
        migrations.AlterField(
            model_name="currencyrate",
            name="buy",
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name="currencyrate",
            name="sell",
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]