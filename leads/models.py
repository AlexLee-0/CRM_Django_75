from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse

from advertisements.models import Advertisement

phone_validator = RegexValidator(
    regex=r"^\+?[0-9\s\-()]{5,20}$",
    message="Введите телефон в формате +7 900 111-22-33 (только цифры, пробелы, дефисы и скобки).",
)


class Lead(models.Model):
    """Потенциальный клиент, узнавший об услуге из рекламной кампании."""

    first_name = models.CharField("Имя", max_length=100)
    last_name = models.CharField("Фамилия", max_length=100)
    phone = models.CharField("Телефон", max_length=32, validators=[phone_validator])
    email = models.EmailField("Email")
    ad = models.ForeignKey(
        Advertisement,
        on_delete=models.PROTECT,
        related_name="leads",
        verbose_name="Рекламная кампания",
    )

    class Meta:
        verbose_name = "Потенциальный клиент"
        verbose_name_plural = "Потенциальные клиенты"
        ordering = ["last_name", "first_name"]

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

    def get_absolute_url(self):
        return reverse("leads:detail", kwargs={"pk": self.pk})
