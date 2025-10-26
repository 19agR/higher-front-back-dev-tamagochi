"""Модуль с исключениями."""


class TamagochiIsGone(Exception):
    """Ошибка при смерти тамагочи."""


class NotEnoughMoney(Exception):
    """Ошибка когда не хватает монет для покупки."""


class IncorrectAnswer(Exception):
    """Ошибка при некорректном выборе ответа."""


class GameExit(Exception):
    """Ошибка для выхода из игры."""


class IsEmpty(Exception):
    """Ошибка при обращении к пустому списку объектов (еда, медикаменты)."""
