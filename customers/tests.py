# pylint: disable=redefined-outer-name,unused-argument
import pytest

from customers.models import Customer
from leads.models import Lead


@pytest.mark.django_db
def test_create_page_prefills_lead_only(client, user_with_role, lead, contract):
    client.force_login(user_with_role("Менеджер"))
    response = client.get(f"/customers/new/?lead={lead.pk}")
    assert response.status_code == 200
    form = response.context["form"]
    assert form.initial["lead"] == lead.pk
    assert not form.initial.get("contract")


@pytest.mark.django_db
def test_manager_converts_lead_to_customer(client, user_with_role, lead, contract):
    client.force_login(user_with_role("Менеджер"))
    response = client.post("/customers/new/", {"lead": lead.pk, "contract": contract.pk})
    assert response.status_code == 302
    assert Customer.objects.get().lead == lead


@pytest.mark.django_db
def test_converted_lead_is_not_offered_again(client, user_with_role, lead, contract):
    Customer.objects.create(lead=lead, contract=contract)
    client.force_login(user_with_role("Менеджер"))
    form = client.get("/customers/new/").context["form"]
    assert lead not in form.fields["lead"].queryset
    assert contract not in form.fields["contract"].queryset


@pytest.mark.django_db
def test_same_lead_cannot_be_converted_twice(client, user_with_role, lead, contract):
    Customer.objects.create(lead=lead, contract=contract)
    client.force_login(user_with_role("Менеджер"))
    response = client.post("/customers/new/", {"lead": lead.pk, "contract": contract.pk})
    assert response.status_code == 200
    assert Customer.objects.count() == 1


@pytest.mark.django_db
def test_operator_cannot_open_customers(client, user_with_role):
    client.force_login(user_with_role("Оператор"))
    assert client.get("/customers/").status_code == 403


@pytest.mark.django_db
def test_lead_with_customer_cannot_be_deleted(client, superuser, lead, contract):
    Customer.objects.create(lead=lead, contract=contract)
    client.force_login(superuser)
    client.post(f"/leads/{lead.pk}/delete/")
    assert Lead.objects.filter(pk=lead.pk).exists()
