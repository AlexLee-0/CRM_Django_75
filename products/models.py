from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse


class Product(models.Model):
    """Услуга, предоставляемая компанией."""

    name = models.CharField("Название", max_length=255, unique=True)
    description = models.TextField("Описание", blank=True)
    cost = models.DecimalField(
        "Стоимость",
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
    )

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"
        ordering = ["name"]

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("products:detail", kwargs={"pk": self.pk})
