# pylint: disable=redefined-outer-name,unused-argument
from decimal import Decimal

import pytest

from customers.models import Customer
from leads.models import Lead


@pytest.mark.django_db
def test_statistic_counts_leads_customers_and_profit(client, user_with_role, ad, lead, contract):
    Lead.objects.create(
        first_name="Пётр",
        last_name="Петров",
        phone="+79002223344",
        email="petrov@example.com",
        ad=ad,
    )
    Customer.objects.create(lead=lead, contract=contract)

    client.force_login(user_with_role("Оператор"))
    response = client.get("/ads/statistic/")

    assert response.status_code == 200
    stat = response.context["ads"][0]
    assert stat.leads_count == 2
    assert stat.customers_count == 1
    assert stat.profit == Decimal("1.50")  # 1500 дохода / 1000 бюджета


@pytest.mark.django_db
def test_statistic_for_ad_without_customers(client, user_with_role, ad, lead):
    client.force_login(user_with_role("Менеджер"))
    stat = client.get("/ads/statistic/").context["ads"][0]
    assert stat.leads_count == 1
    assert stat.customers_count == 0
    assert stat.profit == Decimal("0.00")


@pytest.mark.django_db
def test_marketer_can_create_ad(client, user_with_role, product):
    client.force_login(user_with_role("Маркетолог"))
    response = client.post(
        "/ads/new/",
        {"name": "Новая", "product": product.pk, "channel": "tv", "budget": "500.00"},
    )
    assert response.status_code == 302
