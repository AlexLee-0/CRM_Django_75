from django import forms

from .models import Lead


class LeadForm(forms.ModelForm):
    """Форма создания и редактирования потенциального клиента."""

    class Meta:
        model = Lead
        fields = ["last_name", "first_name", "phone", "email", "ad"]
