from django.contrib import admin

from .models import Advertisement


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ("name", "product", "channel", "budget")
    list_filter = ("channel", "product")
    search_fields = ("name",)
