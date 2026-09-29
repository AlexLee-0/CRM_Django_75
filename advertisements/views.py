from decimal import Decimal

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Count, Sum
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from crm.mixins import ProtectedDeleteMixin

from .forms import AdvertisementForm
from .models import Advertisement


class AdvertisementListView(PermissionRequiredMixin, ListView):
    """Список рекламных кампаний."""

    model = Advertisement
    permission_required = "advertisements.view_advertisement"
    template_name = "ads/ads-list.html"
    context_object_name = "ads"


class AdvertisementDetailView(PermissionRequiredMixin, DetailView):
    """Детальная страница рекламной кампании."""

    model = Advertisement
    permission_required = "advertisements.view_advertisement"
    template_name = "ads/ads-detail.html"


class AdvertisementCreateView(PermissionRequiredMixin, CreateView):
    """Создание рекламной кампании."""

    model = Advertisement
    form_class = AdvertisementForm
    permission_required = "advertisements.add_advertisement"
    template_name = "ads/ads-create.html"
    success_url = reverse_lazy("advertisements:list")


class AdvertisementUpdateView(PermissionRequiredMixin, UpdateView):
    """Редактирование рекламной кампании."""

    model = Advertisement
    form_class = AdvertisementForm
    permission_required = "advertisements.change_advertisement"
    template_name = "ads/ads-edit.html"
    success_url = reverse_lazy("advertisements:list")


class AdvertisementDeleteView(PermissionRequiredMixin, ProtectedDeleteMixin, DeleteView):
    """Удаление рекламной кампании."""

    model = Advertisement
    permission_required = "advertisements.delete_advertisement"
    template_name = "ads/ads-delete.html"
    success_url = reverse_lazy("advertisements:list")


class AdvertisementStatisticView(PermissionRequiredMixin, ListView):
    """
    Статистика успешности рекламных кампаний.

    Для каждой кампании считаются: число привлечённых лидов, число лидов,
    ставших активными клиентами, и соотношение дохода по контрактам
    к бюджету кампании (атрибут ``profit``).
    """

    model = Advertisement
    permission_required = "advertisements.view_advertisement"
    template_name = "ads/ads-statistic.html"
    context_object_name = "ads"

    def get_queryset(self):
        # Цепочка Advertisement -> Lead -> Customer -> Contract: каждый лид
        # связан не более чем с одним активным клиентом и одним контрактом,
        # поэтому Sum по контрактам не задваивается.
        return (
            super()
            .get_queryset()
            .annotate(
                leads_count=Count("leads", distinct=True),
                customers_count=Count("leads__customer", distinct=True),
                income=Sum("leads__customer__contract__cost"),
            )
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for ad in context["ads"]:
            income = ad.income or Decimal("0")
            ad.profit = round(income / ad.budget, 2) if ad.budget else None
        return context
