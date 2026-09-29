from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from crm.mixins import ProtectedDeleteMixin

from .forms import CustomerForm
from .models import Customer


class CustomerListView(PermissionRequiredMixin, ListView):
    """Список активных клиентов."""

    model = Customer
    permission_required = "customers.view_customer"
    template_name = "customers/customers-list.html"
    context_object_name = "customers"

    def get_queryset(self):
        return super().get_queryset().select_related("lead")


class CustomerDetailView(PermissionRequiredMixin, DetailView):
    """Детальная страница активного клиента."""

    model = Customer
    permission_required = "customers.view_customer"
    template_name = "customers/customers-detail.html"


class CustomerCreateView(PermissionRequiredMixin, CreateView):
    """
    Создание активного клиента.

    Если открыть страницу со ссылкой /customers/new/?lead=<id> (ссылка
    «В активные» в списке лидов), поле «Потенциальный клиент»
    предзаполняется, остальные поля остаются пустыми.
    """

    model = Customer
    form_class = CustomerForm
    permission_required = "customers.add_customer"
    template_name = "customers/customers-create.html"
    success_url = reverse_lazy("customers:list")

    def get_initial(self):
        initial = super().get_initial()
        lead_id = self.request.GET.get("lead", "")
        if lead_id.isdigit():
            initial["lead"] = int(lead_id)
        return initial


class CustomerUpdateView(PermissionRequiredMixin, UpdateView):
    """Редактирование активного клиента."""

    model = Customer
    form_class = CustomerForm
    permission_required = "customers.change_customer"
    template_name = "customers/customers-edit.html"
    success_url = reverse_lazy("customers:list")


class CustomerDeleteView(PermissionRequiredMixin, ProtectedDeleteMixin, DeleteView):
    """Удаление активного клиента."""

    model = Customer
    permission_required = "customers.delete_customer"
    template_name = "customers/customers-delete.html"
    success_url = reverse_lazy("customers:list")
