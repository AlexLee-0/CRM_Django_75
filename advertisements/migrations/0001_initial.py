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
            name="Advertisement",
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
                    "channel",
                    models.CharField(
                        choices=[
                            ("social_media", "Социальные сети"),
                            ("context_ads", "Контекстная реклама"),
                            ("email", "Email-рассылка"),
                            ("outdoor", "Наружная реклама"),
                            ("tv", "Телевидение"),
                            ("other", "Другое"),
                        ],
                        default="other",
                        max_length=20,
                        verbose_name="Канал продвижения",
                    ),
                ),
                (
                    "budget",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=12,
                        validators=[
                            django.core.validators.MinValueValidator(decimal.Decimal("0.01"))
                        ],
                        verbose_name="Бюджет на рекламу",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="advertisements",
                        to="products.product",
                        verbose_name="Рекламируемая услуга",
                    ),
                ),
            ],
            options={
                "verbose_name": "Рекламная кампания",
                "verbose_name_plural": "Рекламные кампании",
                "ordering": ["name"],
            },
        ),
    ]
