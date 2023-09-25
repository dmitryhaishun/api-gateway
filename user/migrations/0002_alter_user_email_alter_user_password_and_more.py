# Generated by Django 4.2.2 on 2023-06-23 22:05

import re

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="email",
            field=models.EmailField(max_length=55, unique=True),
        ),
        migrations.AlterField(
            model_name="user",
            name="password",
            field=models.CharField(
                validators=[
                    django.core.validators.RegexValidator(
                        message="Password must contain at least one uppercase letter, one lowercase letter, one digit,"
                        " and one special character",
                        regex=re.compile(
                            "^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*[!@#$%^&*()_\\-+=<>?[\\]{};:\\/<>,.'\\-_...])"
                            "[A-Za-z\\d!@#$%^&*()_\\-+=<>?[\\]{};:\\/<>,.'\\-_...]{6,20}$"
                        ),
                    )
                ]
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="phone_number",
            field=models.CharField(
                unique=True,
                validators=[
                    django.core.validators.RegexValidator(
                        code="invalid_phone",
                        message="Phone number must start with  +  and contain between 10 and 12 digits",
                        regex=re.compile("^\\+\\d{10,12}$"),
                    )
                ],
            ),
        ),
    ]