from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from advertisements.models import Advertisement
from customers.models import Customer
from leads.models import Lead
from products.models import Product


class IndexView(LoginRequiredMixin, TemplateView):
    """Главная страница с общей статистикой по системе."""

    template_name = "users/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["products_count"] = Product.objects.count()
        context["advertisements_count"] = Advertisement.objects.count()
        context["leads_count"] = Lead.objects.count()
        context["customers_count"] = Customer.objects.count()
        return context
