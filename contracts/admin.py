from django.contrib import admin

from .models import Contract


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ("name", "product", "start_date", "end_date", "cost")
    list_filter = ("product",)
    search_fields = ("name",)
