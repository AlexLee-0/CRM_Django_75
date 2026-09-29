# pylint: disable=redefined-outer-name,unused-argument
import pytest
from django.core.files.uploadedfile import SimpleUploadedFile

from contracts.models import Contract


def _payload(product, **overrides):
    data = {
        "name": "Договор №5",
        "product": product.pk,
        "start_date": "2026-03-01",
        "end_date": "2026-09-01",
        "cost": "2000.00",
        "document": SimpleUploadedFile("contract.pdf", b"%PDF-1.4 test"),
    }
    data.update(overrides)
    return data


@pytest.mark.django_db
def test_manager_creates_contract_with_file(client, user_with_role, product):
    client.force_login(user_with_role("Менеджер"))
    response = client.post("/contracts/new/", _payload(product))
    assert response.status_code == 302
    contract = Contract.objects.get(name="Договор №5")
    assert contract.document.name.startswith("contracts/")


@pytest.mark.django_db
def test_end_date_before_start_date_rejected(client, user_with_role, product):
    client.force_login(user_with_role("Менеджер"))
    response = client.post(
        "/contracts/new/", _payload(product, start_date="2026-09-01", end_date="2026-03-01")
    )
    assert response.status_code == 200
    assert "end_date" in response.context["form"].errors
    assert Contract.objects.count() == 0


@pytest.mark.django_db
def test_operator_has_no_access_to_contracts(client, user_with_role):
    client.force_login(user_with_role("Оператор"))
    assert client.get("/contracts/").status_code == 403
