from django import forms

from .models import Advertisement


class AdvertisementForm(forms.ModelForm):
    """Форма создания и редактирования рекламной кампании."""

    class Meta:
        model = Advertisement
        fields = ["name", "product", "channel", "budget"]
