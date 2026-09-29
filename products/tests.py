# pylint: disable=redefined-outer-name,unused-argument
import pytest
from django.contrib.messages import get_messages

from products.models import Product


@pytest.mark.django_db
def test_anonymous_redirected_to_login(client):
    response = client.get("/products/")
    assert response.status_code == 302
    assert response.url.startswith("/accounts/login/")


@pytest.mark.django_db
def test_operator_has_no_access_to_products(client, user_with_role):
    client.force_login(user_with_role("Оператор"))
    assert client.get("/products/").status_code == 403


@pytest.mark.django_db
def test_marketer_creates_product(client, user_with_role):
    client.force_login(user_with_role("Маркетолог"))
    response = client.post(
        "/products/new/", {"name": "Аудит", "description": "Полный аудит", "cost": "3000.00"}
    )
    assert response.status_code == 302
    assert Product.objects.filter(name="Аудит").exists()


@pytest.mark.django_db
def test_product_cost_must_be_positive(client, user_with_role):
    client.force_login(user_with_role("Маркетолог"))
    response = client.post("/products/new/", {"name": "Бесплатно", "description": "", "cost": "0"})
    assert response.status_code == 200
    assert "cost" in response.context["form"].errors


@pytest.mark.django_db
def test_marketer_cannot_delete_product(client, user_with_role, product):
    client.force_login(user_with_role("Маркетолог"))
    assert client.post(f"/products/{product.pk}/delete/").status_code == 403
    assert Product.objects.filter(pk=product.pk).exists()


@pytest.mark.django_db
def test_protected_product_is_not_deleted(client, superuser, ad):
    client.force_login(superuser)
    response = client.post(f"/products/{ad.product.pk}/delete/")
    assert response.status_code == 302
    assert Product.objects.filter(pk=ad.product.pk).exists()
    messages = [str(m) for m in get_messages(response.wsgi_request)]
    assert any("Нельзя удалить" in m for m in messages)


@pytest.mark.django_db
def test_unknown_product_returns_404(client, superuser):
    client.force_login(superuser)
    assert client.get("/products/9999/").status_code == 404
