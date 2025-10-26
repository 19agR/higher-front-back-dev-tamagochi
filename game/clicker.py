import random
from string import ascii_uppercase
from abc import ABC, abstractmethod

"""Модуль с интерфейсом и реализацией кликера."""


class AbstractClicker(ABC):
    """Интерфейс для кликера."""

    @abstractmethod
    def __init__(self) -> None:
        """Абстрактный метод инициализации."""
        raise NotImplementedError

    @abstractmethod
    def click(self) -> None:
        """Абстрактный метод клика для накапливания монет."""
        raise NotImplementedError

    @property
    @abstractmethod
    def income_per_click(self) -> int:
        """Абстрактное свойство для доступа к количеству монет за клик."""
        raise NotImplementedError

    @property
    @abstractmethod
    def get_work_description(self) -> str:
        """Абстрактное свойство для доступа к описанию сути кликера."""
        raise NotImplementedError


class RandomSymbolsClicker(AbstractClicker):
    """
    Интерфейс для кликера.
    Это клавиатурный кликер, в котором нужно нажимать на кнопки для заработка.
    """

    def __init__(self, income_per_click=10, symbols=ascii_uppercase) -> None:
        """Создание необходимых для работы кликера параметров"""
        # Символы для выборки работы
        self.symbols = symbols.lower()
        self._income_per_click = income_per_click
        self._work_description = ('Вы работаете в службе по набору текста '
                                  'и вам необходимо помогать людям набирать '
                                  'текст на их клавиатуре, наша программа '
                                  'тайно подключает вас к случайному пользователю, '
                                  'которому требуется помощь. Что ж, надеюсь вы'
                                  ' не подведете. Удачи!')

    def click(self) -> bool:
        """Метод клика для накапливания монет."""
        symbol = random.choice(self.symbols)
        while True:
            answer = input(f'Введите символ {symbol}: ').lower().strip()
            if answer == 'exit':
                return False
            if answer == symbol:
                print('Все верно! Продолжайте в том же духе =)')
                break
            print('Неверно! Попробуйте снова (буквы написаны на английском)')
        return True

    @property
    def income_per_click(self) -> int:
        """Свойство для доступа к количеству монет за клик."""
        return self._income_per_click

    @property
    def get_work_description(self) -> str:
        """Свойство для доступа к описанию сути кликера."""
        return self._work_description



