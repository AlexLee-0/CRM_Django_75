# pylint: disable=redefined-outer-name,unused-argument
import pytest


@pytest.mark.django_db
def test_index_requires_login(client):
    response = client.get("/")
    assert response.status_code == 302
    assert response.url.startswith("/accounts/login/")


@pytest.mark.django_db
def test_index_shows_counts(client, user_with_role, lead):
    client.force_login(user_with_role("Оператор"))
    response = client.get("/")
    assert response.status_code == 200
    assert response.context["leads_count"] == 1
    assert response.context["products_count"] == 1
    assert response.context["customers_count"] == 0


@pytest.mark.django_db
def test_login_success_and_failure(client, superuser):
    response = client.post(
        "/accounts/login/", {"username": "root", "password": "pass12345"}
    )
    assert response.status_code == 302
    assert response.url == "/"

    response = client.post("/accounts/login/", {"username": "root", "password": "wrong"})
    assert response.status_code == 200  # форма с ошибкой, вход не выполнен


@pytest.mark.django_db
def test_roles_fixture_permissions(user_with_role):
    operator = user_with_role("Оператор")
    assert operator.has_perm("leads.add_lead")
    assert not operator.has_perm("leads.delete_lead")
    assert not operator.has_perm("products.view_product")
    assert operator.has_perm("advertisements.view_advertisement")
