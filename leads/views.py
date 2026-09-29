from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from crm.mixins import ProtectedDeleteMixin

from .forms import LeadForm
from .models import Lead


class LeadListView(PermissionRequiredMixin, ListView):
    """Список потенциальных клиентов."""

    model = Lead
    permission_required = "leads.view_lead"
    template_name = "leads/leads-list.html"
    context_object_name = "leads"

    def get_queryset(self):
        # select_related убирает N+1 при проверке «уже активный клиент?»
        return super().get_queryset().select_related("customer")


class LeadDetailView(PermissionRequiredMixin, DetailView):
    """Детальная страница потенциального клиента."""

    model = Lead
    permission_required = "leads.view_lead"
    template_name = "leads/leads-detail.html"


class LeadCreateView(PermissionRequiredMixin, CreateView):
    """Создание потенциального клиента."""

    model = Lead
    form_class = LeadForm
    permission_required = "leads.add_lead"
    template_name = "leads/leads-create.html"
    success_url = reverse_lazy("leads:list")


class LeadUpdateView(PermissionRequiredMixin, UpdateView):
    """Редактирование потенциального клиента."""

    model = Lead
    form_class = LeadForm
    permission_required = "leads.change_lead"
    template_name = "leads/leads-edit.html"
    success_url = reverse_lazy("leads:list")


class LeadDeleteView(PermissionRequiredMixin, ProtectedDeleteMixin, DeleteView):
    """Удаление потенциального клиента."""

    model = Lead
    permission_required = "leads.delete_lead"
    template_name = "leads/leads-delete.html"
    success_url = reverse_lazy("leads:list")
