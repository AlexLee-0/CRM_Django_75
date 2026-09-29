from django import forms

from .models import Contract


class ContractForm(forms.ModelForm):
    """Форма создания и редактирования контракта."""

    class Meta:
        model = Contract
        fields = ["name", "product", "document", "start_date", "end_date", "cost"]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "end_date": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
        }
