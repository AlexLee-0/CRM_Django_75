# pylint: disable=redefined-outer-name,unused-argument
import pytest

from leads.models import Lead


@pytest.mark.django_db
def test_operator_creates_lead(client, user_with_role, ad):
    client.force_login(user_with_role("Оператор"))
    response = client.post(
        "/leads/new/",
        {
            "last_name": "Сидоров",
            "first_name": "Алексей",
            "phone": "+7 900 333-44-55",
            "email": "sidorov@example.com",
            "ad": ad.pk,
        },
    )
    assert response.status_code == 302
    assert Lead.objects.filter(last_name="Сидоров").exists()


@pytest.mark.django_db
def test_invalid_phone_and_email_rejected(client, user_with_role, ad):
    client.force_login(user_with_role("Оператор"))
    response = client.post(
        "/leads/new/",
        {"last_name": "А", "first_name": "Б", "phone": "abc", "email": "not-an-email", "ad": ad.pk},
    )
    assert response.status_code == 200
    errors = response.context["form"].errors
    assert "phone" in errors
    assert "email" in errors
    assert Lead.objects.count() == 0


@pytest.mark.django_db
def test_marketer_cannot_see_leads(client, user_with_role):
    client.force_login(user_with_role("Маркетолог"))
    assert client.get("/leads/").status_code == 403


@pytest.mark.django_db
def test_manager_sees_convert_link_but_operator_does_not(client, user_with_role, lead):
    client.force_login(user_with_role("Менеджер"))
    html = client.get("/leads/").content.decode()
    assert f"/customers/new/?lead={lead.pk}" in html

    client.force_login(user_with_role("Оператор"))
    html = client.get("/leads/").content.decode()
    assert "/customers/new/" not in html


@pytest.mark.django_db
def test_operator_cannot_delete_lead(client, user_with_role, lead):
    client.force_login(user_with_role("Оператор"))
    assert client.post(f"/leads/{lead.pk}/delete/").status_code == 403
