import random
from string import ascii_uppercase

from game.tamagochi import AbstractTamagochi

"""Модуль с интерфейсом и реализацией кликера"""

from abc import ABC, abstractmethod


class AbstractClicker(ABC):
    """Интерфейс для кликера"""

    @abstractmethod
    def __init__(self) -> None:
        """Абстрактный метод инициализации"""
        raise NotImplementedError

    @abstractmethod
    def click(self) -> None:
        """Абстрактный метод клика для накапливания монет"""
        raise NotImplementedError

    @property
    @abstractmethod
    def income_per_click(self) -> int:
        """Абстрактное свойство для доступа к количеству монет за клик"""
        raise NotImplementedError

    @property
    @abstractmethod
    def get_work_description(self) -> str:
        """Абстрактное свойство для доступа к описанию сути кликера"""
        raise NotImplementedError


class RandomSymbolsClicker(AbstractClicker):
    def __init__(self, income_per_click=5, symbols=ascii_uppercase) -> None:
        # Символы для выборки работы
        self.symbols = symbols
        self._income_per_click = income_per_click
        self._work_description = ('Вы работаете в службе по набору текста '
                                  'и вам необходимо помогать людям набирать '
                                  'текст на их клавиатуре, наша программа '
                                  'тайно подключает вас к случайному пользователю, '
                                  'которому требуется помощь. Что ж, надеюсь вы'
                                  ' не подведете. Удачи!')

    def click(self) -> None:
        symbol = random.choice(self.symbols)
        while input(f'Введите символ {symbol}: ') != symbol:
            print('Неверно! Попробуйте снова (раскладка должно быть английская)')

    @property
    def income_per_click(self) -> int:
        return self._income_per_click

    @property
    def get_work_description(self) -> str:
        return self._work_description



