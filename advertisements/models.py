from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse

from products.models import Product


class Advertisement(models.Model):
    """Рекламная кампания по продвижению услуги."""

    class Channel(models.TextChoices):
        """Каналы продвижения."""

        SOCIAL_MEDIA = "social_media", "Социальные сети"
        CONTEXT_ADS = "context_ads", "Контекстная реклама"
        EMAIL = "email", "Email-рассылка"
        OUTDOOR = "outdoor", "Наружная реклама"
        TV = "tv", "Телевидение"
        OTHER = "other", "Другое"

    name = models.CharField("Название", max_length=255, unique=True)
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name="advertisements",
        verbose_name="Рекламируемая услуга",
    )
    channel = models.CharField(
        "Канал продвижения",
        max_length=20,
        choices=Channel.choices,
        default=Channel.OTHER,
    )
    budget = models.DecimalField(
        "Бюджет на рекламу",
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
    )

    class Meta:
        verbose_name = "Рекламная кампания"
        verbose_name_plural = "Рекламные кампании"
        ordering = ["name"]

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("advertisements:detail", kwargs={"pk": self.pk})
