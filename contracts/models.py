from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse

from products.models import Product


class Contract(models.Model):
    """Контракт на предоставление услуги."""

    name = models.CharField("Название", max_length=255, unique=True)
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name="contracts",
        verbose_name="Предоставляемая услуга",
    )
    document = models.FileField("Файл с документом", upload_to="contracts/")
    start_date = models.DateField("Дата заключения")
    end_date = models.DateField("Дата окончания действия")
    cost = models.DecimalField(
        "Сумма",
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
    )

    class Meta:
        verbose_name = "Контракт"
        verbose_name_plural = "Контракты"
        ordering = ["-start_date", "name"]

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("contracts:detail", kwargs={"pk": self.pk})

    def clean(self):
        super().clean()
        if self.start_date and self.end_date and self.end_date < self.start_date:
            raise ValidationError(
                {"end_date": "Дата окончания не может быть раньше даты заключения."}
            )
