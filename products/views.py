from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from crm.mixins import ProtectedDeleteMixin

from .forms import ProductForm
from .models import Product


class ProductListView(PermissionRequiredMixin, ListView):
    """Список услуг."""

    model = Product
    permission_required = "products.view_product"
    template_name = "products/products-list.html"
    context_object_name = "products"


class ProductDetailView(PermissionRequiredMixin, DetailView):
    """Детальная страница услуги."""

    model = Product
    permission_required = "products.view_product"
    template_name = "products/products-detail.html"


class ProductCreateView(PermissionRequiredMixin, CreateView):
    """Создание услуги."""

    model = Product
    form_class = ProductForm
    permission_required = "products.add_product"
    template_name = "products/products-create.html"
    success_url = reverse_lazy("products:list")


class ProductUpdateView(PermissionRequiredMixin, UpdateView):
    """Редактирование услуги."""

    model = Product
    form_class = ProductForm
    permission_required = "products.change_product"
    template_name = "products/products-edit.html"
    success_url = reverse_lazy("products:list")


class ProductDeleteView(PermissionRequiredMixin, ProtectedDeleteMixin, DeleteView):
    """Удаление услуги."""

    model = Product
    permission_required = "products.delete_product"
    template_name = "products/products-delete.html"
    success_url = reverse_lazy("products:list")
