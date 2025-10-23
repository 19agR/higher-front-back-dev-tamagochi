"""Модуль с интерфейсом и реализацией класса игры"""

from abc import ABC, abstractmethod
from typing import Any

from .tamagochi import AbstractTamagochi
from .clicker import AbstractClicker, RandomSymbolsClicker
from .models import Food, Medicine


class AbstractGame(ABC):
    """Интерфейс для логики игры"""

    @abstractmethod
    def __init__(
        self,
        tamagochi: AbstractTamagochi,
        clicker: AbstractClicker,
        all_food: list[Food],
        all_medicine: list[Medicine]
    ):
        """
        Абстрактный метод инициализации класса игры

        :param tamagochi: экземпляр тамагочи
        :param clicker: экземпляр кликера
        :param all_food: все доступные варианты еды
        :param all_medicine: все доступные варианты лекарств
        """
        raise NotImplementedError

    @abstractmethod
    def work(self) -> int:
        """
        Абстрактный метод для логики действия "работа"

        :return: количество заработанных монет
        """
        raise NotImplementedError

    @abstractmethod
    def buy_food(self) -> None:
        """Абстрактный метод для покупки еды"""
        raise NotImplementedError

    @abstractmethod
    def buy_medicine(self) -> None:
        """Абстрактный метод для покупки лекарства"""
        raise NotImplementedError

    @abstractmethod
    def feed_tamagochi(self) -> None:
        """Абстрактный метод для кормления тамагочи"""
        raise NotImplementedError

    @abstractmethod
    def heal_tamagochi(self) -> None:
        """Абстрактный метод для лечения тамагочи"""
        raise NotImplementedError

    @abstractmethod
    def rest_tamagochi(self):
        """Абстрактный метод для отдыха тамагочи"""
        raise NotImplementedError

    @abstractmethod
    def play_with_tamagochi(self):
        """Абстрактный метод для игры с тамагочи"""
        raise NotImplementedError

    @abstractmethod
    def get_status(self) -> dict[str, Any]:
        """
        Абстрактный метод для получения статуса (всех характеристик) тамагочи

        :return: словарь со всеми характеристиками тамагочи
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def food(self) -> list[Food]:
        """
        Абстрактное свойство для доступа к сумке с едой

        :return: список с имеющимися (купленными) объектами еды
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def medicine(self) -> list[Medicine]:
        """
        Абстрактное свойство для доступа к сумке с лекарствами

        :return: список с имеющимися (купленными) объектами лекарств
        """
        raise NotImplementedError


class NormalGame(AbstractGame):
    """Интерфейс для логики игры"""

    def __init__(
            self,
            tamagochi: AbstractTamagochi,
            clicker: AbstractClicker,
            all_food: list[Food],
            all_medicine: list[Medicine]
    ):
        """
        Абстрактный метод инициализации класса игры

        :param tamagochi: экземпляр тамагочи
        :param clicker: экземпляр кликера
        :param all_food: все доступные варианты еды
        :param all_medicine: все доступные варианты лекарств
        """
        self.tamagochi = tamagochi
        self.clicker = clicker
        self.all_food = all_food
        self.all_medicine = all_medicine

        self.storage_food = []
        self.storage_medicine = []
        self.storage_money = 150

    def work(self) -> int:
        """
        Абстрактный метод для логики действия "работа"

        :return: количество заработанных монет
        """
        print('Добро пожаловать на работу! Ну что ж, давайте приступать.\n'
              f'{self.clicker.get_work_description}')

        self.clicker.click()
        return self.clicker.income_per_click


    def buy_food(self) -> None:
        """Абстрактный метод для покупки еды"""
        all_food_str = '\n'.join(
            f'{i + 1}. {self.all_food[i]}'
            for i in range(len(self.all_food))
        ) + f'\n{len(self.all_food) + 1}. Вернуться назад'
        print(all_food_str)
        if (answer := input('Что выбираете?: ')).isdigit() and (answer := int(answer)) <= len(self.all_food) + 1:
            if answer == len(self.all_food) + 1:  # вернуться назад
                return
            selected_food = self.all_food[answer - 1]
            if selected_food.price <= self.storage_money:
                self.storage_food.append(selected_food)
                self.storage_money -= selected_food.price
                print(f'Еда "{selected_food.name}" добавлена в холодильник!')
            else:
                print(f'Упс, кажется монеток на счету не хватило для оплаты...\n'
                      f'Монеток на счету: {self.storage_money}')
        else:
            print('Упс, кажется такого варианта не было. Попробуйте снова!')
            self.buy_food()
### делаем свои ошибки

    def buy_medicine(self) -> None:
        """Абстрактный метод для покупки лекарства"""

    def feed_tamagochi(self) -> None:
        """Абстрактный метод для кормления тамагочи"""

    def heal_tamagochi(self) -> None:
        """Абстрактный метод для лечения тамагочи"""

    def rest_tamagochi(self):
        """Абстрактный метод для отдыха тамагочи"""

    def play_with_tamagochi(self):
        """Абстрактный метод для игры с тамагочи"""

    def get_status(self) -> dict[str, Any]:
        """
        Абстрактный метод для получения статуса (всех характеристик) тамагочи

        :return: словарь со всеми характеристиками тамагочи
        """

    @property
    def food(self) -> list[Food]:
        """
        Абстрактное свойство для доступа к сумке с едой

        :return: список с имеющимися (купленными) объектами еды
        """
        return self.storage_food


    @property
    def medicine(self) -> list[Medicine]:
        """
        Абстрактное свойство для доступа к сумке с лекарствами

        :return: список с имеющимися (купленными) объектами лекарств
        """
        return self.storage_medicine
