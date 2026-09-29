"""Общие миксины для представлений CRM-системы."""

from django.contrib import messages
from django.db.models import ProtectedError
from django.http import HttpResponseRedirect


class ProtectedDeleteMixin:
    """
    Перехватывает ProtectedError при удалении.

    Связи между объектами защищены on_delete=PROTECT, поэтому, например,
    услугу с рекламными кампаниями удалить нельзя. Вместо ошибки 500
    пользователь получает понятное сообщение и возвращается к списку.
    """

    def form_valid(self, form):  # pylint: disable=missing-function-docstring
        try:
            return super().form_valid(form)  # pylint: disable=no-member
        except ProtectedError:
            messages.error(
                self.request,
                f"Нельзя удалить «{self.object}»: на эту запись ссылаются другие "
                "объекты. Сначала удалите или измените связанные записи.",
            )
            return HttpResponseRedirect(self.get_success_url())
