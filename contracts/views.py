from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from crm.mixins import ProtectedDeleteMixin

from .forms import ContractForm
from .models import Contract


class ContractListView(PermissionRequiredMixin, ListView):
    """Список контрактов."""

    model = Contract
    permission_required = "contracts.view_contract"
    template_name = "contracts/contracts-list.html"
    context_object_name = "contracts"


class ContractDetailView(PermissionRequiredMixin, DetailView):
    """Детальная страница контракта."""

    model = Contract
    permission_required = "contracts.view_contract"
    template_name = "contracts/contracts-detail.html"


class ContractCreateView(PermissionRequiredMixin, CreateView):
    """Создание контракта."""

    model = Contract
    form_class = ContractForm
    permission_required = "contracts.add_contract"
    template_name = "contracts/contracts-create.html"
    success_url = reverse_lazy("contracts:list")


class ContractUpdateView(PermissionRequiredMixin, UpdateView):
    """Редактирование контракта."""

    model = Contract
    form_class = ContractForm
    permission_required = "contracts.change_contract"
    template_name = "contracts/contracts-edit.html"
    success_url = reverse_lazy("contracts:list")


class ContractDeleteView(PermissionRequiredMixin, ProtectedDeleteMixin, DeleteView):
    """Удаление контракта."""

    model = Contract
    permission_required = "contracts.delete_contract"
    template_name = "contracts/contracts-delete.html"
    success_url = reverse_lazy("contracts:list")
