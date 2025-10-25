"""Модуль с интерфейсом и реализацией класса игры"""

from abc import ABC, abstractmethod
from typing import Any

from .exceptions import IncorrectAnswer, NotEnoughMoney
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

        self.first_time_on_work = True

    def work(self) -> int:
        """
        Абстрактный метод для логики действия "работа"

        :return: количество заработанных монет
        """
        if self.first_time_on_work:
            print('Добро пожаловать на работу! Ну что ж, давайте приступать.\n'
                  f'{self.clicker.get_work_description}\n'
                  f'Когда захотите закончить работу, напишите "exit"')
            self.first_time_on_work = False
        else:
            print('Рады видеть вас снова! Думаю вы помните что надо делать\n'
                  f'Когда захотите закончить работу, напишите "exit"')

        earned_money = 0
        while True:
            result = self.clicker.click()
            if result:
                earned_money += self.clicker.income_per_click
            else:
                break
        self.storage_money += earned_money
        return earned_money

    def buy_food(self) -> str:
        """Абстрактный метод для покупки еды"""
        result = self.go_to_shop(self.all_food, self.storage_food)
        return result if result else ''

    def buy_medicine(self) -> str:
        """Абстрактный метод для покупки лекарства"""
        result = self.go_to_shop(self.all_medicine, self.storage_medicine)
        return result if result else ''

    def go_to_shop(self, products, storage) -> str | None:
        products_str = self.get_options_from_list(products)
        print(products_str)
        if (answer := input('Что выбираете?: ')).isdigit() and (
        answer := int(answer)) <= len(products) + 1:
            if answer == len(products) + 1:  # вернуться назад
                return None
            selected_food = products[answer - 1]

            if selected_food.price <= self.storage_money:
                self.storage_money -= selected_food.price
                storage.append(selected_food)
                return f'Еда "{selected_food.name}" добавлена в холодильник!'
            else:
                raise NotEnoughMoney('Недостаточно монет')
        else:
            raise IncorrectAnswer('Неверный ответ')

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

    @staticmethod
    def get_options_from_list(objects) -> str:
        return '\n'.join(
            f'{i + 1}. {objects[i]}'
            for i in range(len(objects))
        ) + f'\n{len(objects) + 1}. Вернуться назад'

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


