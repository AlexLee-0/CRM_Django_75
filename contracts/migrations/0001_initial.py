import decimal

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("products", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Contract",
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
                (
                    "document",
                    models.FileField(upload_to="contracts/", verbose_name="Файл с документом"),
                ),
                ("start_date", models.DateField(verbose_name="Дата заключения")),
                ("end_date", models.DateField(verbose_name="Дата окончания действия")),
                (
                    "cost",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=12,
                        validators=[
                            django.core.validators.MinValueValidator(decimal.Decimal("0.01"))
                        ],
                        verbose_name="Сумма",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="contracts",
                        to="products.product",
                        verbose_name="Предоставляемая услуга",
                    ),
                ),
            ],
            options={
                "verbose_name": "Контракт",
                "verbose_name_plural": "Контракты",
                "ordering": ["-start_date", "name"],
            },
        ),
    ]
