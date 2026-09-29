"""Корневая конфигурация URL проекта CRM-системы."""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "accounts/login/",
        auth_views.LoginView.as_view(template_name="registration/login.html"),
        name="login",
    ),
    path("accounts/logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("", include("users.urls")),
    path("products/", include("products.urls")),
    path("ads/", include("advertisements.urls")),
    path("leads/", include("leads.urls")),
    path("contracts/", include("contracts.urls")),
    path("customers/", include("customers.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
