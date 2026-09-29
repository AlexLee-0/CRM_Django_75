from django.contrib import admin

from .models import Lead


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ("last_name", "first_name", "phone", "email", "ad")
    list_filter = ("ad",)
    search_fields = ("last_name", "first_name", "phone", "email")
