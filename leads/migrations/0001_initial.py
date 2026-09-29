import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("advertisements", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Lead",
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
                ("first_name", models.CharField(max_length=100, verbose_name="Имя")),
                ("last_name", models.CharField(max_length=100, verbose_name="Фамилия")),
                (
                    "phone",
                    models.CharField(
                        max_length=32,
                        validators=[
                            django.core.validators.RegexValidator(
                                message="Введите телефон в формате +7 900 111-22-33 (только цифры, пробелы, дефисы и скобки).",
                                regex="^\\+?[0-9\\s\\-()]{5,20}$",
                            )
                        ],
                        verbose_name="Телефон",
                    ),
                ),
                ("email", models.EmailField(max_length=254, verbose_name="Email")),
                (
                    "ad",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="leads",
                        to="advertisements.advertisement",
                        verbose_name="Рекламная кампания",
                    ),
                ),
            ],
            options={
                "verbose_name": "Потенциальный клиент",
                "verbose_name_plural": "Потенциальные клиенты",
                "ordering": ["last_name", "first_name"],
            },
        ),
    ]
