# pylint: disable=redefined-outer-name,unused-argument
"""Общие фикстуры pytest для тестов CRM-системы."""

import datetime
from decimal import Decimal

import pytest
from django.contrib.auth.models import Group, User
from django.core.management import call_command

from advertisements.models import Advertisement
from contracts.models import Contract
from leads.models import Lead
from products.models import Product


@pytest.fixture(autouse=True)
def media_root(settings, tmp_path):
    """Файлы, загружаемые в тестах, попадают во временную папку."""
    settings.MEDIA_ROOT = tmp_path


@pytest.fixture
def roles(db):
    """Загружает преднастроенные роли (группы с правами) из фикстуры."""
    call_command("loaddata", "roles", verbosity=0)


@pytest.fixture
def user_with_role(roles):
    """Фабрика: создаёт пользователя и добавляет его в группу-роль."""

    def _make(group_name):
        user = User.objects.create_user(username=group_name, password="pass12345")
        user.groups.add(Group.objects.get(name=group_name))
        return user

    return _make


@pytest.fixture
def superuser(db):
    return User.objects.create_superuser(username="root", password="pass12345")


@pytest.fixture
def product(db):
    return Product.objects.create(name="SEO", description="Продвижение", cost=Decimal("8000.00"))


@pytest.fixture
def ad(product):
    return Advertisement.objects.create(
        name="Весенняя акция",
        product=product,
        channel=Advertisement.Channel.EMAIL,
        budget=Decimal("1000.00"),
    )


@pytest.fixture
def lead(ad):
    return Lead.objects.create(
        first_name="Иван",
        last_name="Иванов",
        phone="+79001112233",
        email="ivanov@example.com",
        ad=ad,
    )


@pytest.fixture
def contract(product):
    return Contract.objects.create(
        name="Договор №1",
        product=product,
        document="contracts/doc.txt",
        start_date=datetime.date(2026, 1, 1),
        end_date=datetime.date(2026, 12, 31),
        cost=Decimal("1500.00"),
    )
