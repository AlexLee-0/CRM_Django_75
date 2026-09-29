from django.db import models
from django.urls import reverse

from contracts.models import Contract
from leads.models import Lead


class Customer(models.Model):
    """
    Активный клиент.

    Создаётся только на основе существующего потенциального клиента (Lead)
    и заключённого с ним контракта (Contract).
    """

    lead = models.OneToOneField(
        Lead,
        on_delete=models.PROTECT,
        related_name="customer",
        verbose_name="Потенциальный клиент",
    )
    contract = models.OneToOneField(
        Contract,
        on_delete=models.PROTECT,
        related_name="customer",
        verbose_name="Контракт",
    )

    class Meta:
        verbose_name = "Активный клиент"
        verbose_name_plural = "Активные клиенты"
        ordering = ["lead__last_name", "lead__first_name"]

    def __str__(self):
        return str(self.lead)

    def get_absolute_url(self):
        return reverse("customers:detail", kwargs={"pk": self.pk})
