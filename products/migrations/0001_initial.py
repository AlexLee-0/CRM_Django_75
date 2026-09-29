import decimal

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(max_length=255, unique=True, verbose_name="Название"),
                ),
                ("description", models.TextField(blank=True, verbose_name="Описание")),
                (
                    "cost",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=12,
                        validators=[
                            django.core.validators.MinValueValidator(decimal.Decimal("0.01"))
                        ],
                        verbose_name="Стоимость",
                    ),
                ),
            ],
            options={
                "verbose_name": "Услуга",
                "verbose_name_plural": "Услуги",
                "ordering": ["name"],
            },
        ),
    ]
