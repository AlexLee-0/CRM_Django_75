from django import forms
from django.db.models import Q

from contracts.models import Contract
from leads.models import Lead

from .models import Customer


class CustomerForm(forms.ModelForm):
    """
    Форма создания и редактирования активного клиента.

    В списках выбора остаются только лиды и контракты, которые ещё не
    привязаны к активному клиенту (плюс текущие значения при редактировании).
    """

    class Meta:
        model = Customer
        fields = ["lead", "contract"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        free_leads = Q(customer__isnull=True)
        free_contracts = Q(customer__isnull=True)
        if self.instance.pk:
            free_leads |= Q(pk=self.instance.lead_id)
            free_contracts |= Q(pk=self.instance.contract_id)
        self.fields["lead"].queryset = Lead.objects.filter(free_leads)
        self.fields["contract"].queryset = Contract.objects.filter(free_contracts)
