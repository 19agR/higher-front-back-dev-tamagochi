"""Модуль с интерфейсом и реализацией класса игры."""

from abc import ABC, abstractmethod
from typing import Any

from .exceptions import IncorrectAnswer, NotEnoughMoney, IsEmpty
from .tamagochi import AbstractTamagochi
from .clicker import AbstractClicker
from .models import Food, Medicine


class AbstractGame(ABC):
    """Интерфейс для логики игры."""

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
        :param all_medicine: все доступные варианты лекарств.
        """
        raise NotImplementedError

    @abstractmethod
    def work(self) -> int:
        """
        Абстрактный метод для логики действия "работа"

        :return: количество заработанных монет.
        """
        raise NotImplementedError

    @abstractmethod
    def buy_food(self) -> None:
        """Абстрактный метод для покупки еды."""
        raise NotImplementedError

    @abstractmethod
    def buy_medicine(self) -> None:
        """Абстрактный метод для покупки лекарства."""
        raise NotImplementedError

    @abstractmethod
    def go_to_shop(self, products, storage) -> str | None:
        """Абстрактный метод для покупки предмета и складывания в хранилище."""
        raise NotImplementedError

    @abstractmethod
    def choose_smth(self, objects):
        """Абстрактный метод для выбора предмета из списка объектов."""
        raise NotImplementedError

    @abstractmethod
    def feed_tamagochi(self) -> None:
        """Абстрактный метод для кормления тамагочи."""
        raise NotImplementedError

    @abstractmethod
    def heal_tamagochi(self) -> None:
        """Абстрактный метод для лечения тамагочи."""
        raise NotImplementedError

    @abstractmethod
    def rest_tamagochi(self):
        """Абстрактный метод для отдыха тамагочи."""
        raise NotImplementedError

    @abstractmethod
    def play_with_tamagochi(self):
        """Абстрактный метод для игры с тамагочи."""
        raise NotImplementedError

    @abstractmethod
    def get_status(self) -> dict[str, Any]:
        """
        Абстрактный метод для получения статуса (всех характеристик) тамагочи

        :return: словарь со всеми характеристиками тамагочи.
        """
        raise NotImplementedError

    @abstractmethod
    def restart(self) -> None:
        """Абстрактный метод для рестарта игры."""
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def get_options_from_list(objects) -> str:
        """Абстрактный метод для получения списка для выбора."""
        raise NotImplementedError

    @property
    @abstractmethod
    def work_coef(self) -> float:
        """Абстрактное свойство для доступа к множителю заработанных монет."""
        raise NotImplementedError

    @property
    @abstractmethod
    def food(self) -> list[Food]:
        """
        Абстрактное свойство для доступа к сумке с едой

        :return: список с имеющимися (купленными) объектами еды.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def medicine(self) -> list[Medicine]:
        """
        Абстрактное свойство для доступа к сумке с лекарствами

        :return: список с имеющимися (купленными) объектами лекарств.
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
        Метод инициализации класса игры

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

        self.first_time_on_work = True

    def work(self) -> int:
        """
        Метод для логики действия "работа"

        :return: количество заработанных монет
        """
        if self.first_time_on_work:
            print('Добро пожаловать на работу! Ну что ж, давайте приступать.\n'
                  f'{self.clicker.get_work_description}\n'
                  f'Когда захотите закончить работу, напишите "exit"')
            self.first_time_on_work = False
        else:
            print('Рады видеть вас снова! Думаю вы помните что надо делать\n'
                  'Когда захотите закончить работу, напишите "exit"')

        earned_money = 0
        while True:
            result = self.clicker.click()
            if result:
                earned_money += self.clicker.income_per_click * self.work_coef
                self.tamagochi.work()
                output = self.tamagochi.update()
                if output:
                    print(output)
            else:
                break
        self.tamagochi.change_feature('coins', earned_money)
        return earned_money

    def buy_food(self) -> str:
        """Метод для покупки еды"""
        result = self.go_to_shop(self.all_food, self.storage_food)
        return result if result else ''

    def buy_medicine(self) -> str:
        """Метод для покупки лекарства"""
        result = self.go_to_shop(self.all_medicine, self.storage_medicine)
        return result if result else ''

    def go_to_shop(self, products, storage) -> str | None:
        """Метод для покупки предмета и складывания в хранилище."""
        selected_food = self.choose_smth(products)
        if selected_food is None:
            return None

        if selected_food.price <= self.tamagochi.status['coins']:
            self.tamagochi.change_feature('coins', -selected_food.price)
            storage.append(selected_food)
            return f'Еда "{selected_food.name}" добавлена в холодильник!'
        else:
            raise NotEnoughMoney('Недостаточно монет')

    def choose_smth(self, objects):
        """Метод для выбора предмета из списка объектов."""
        products_str = self.get_options_from_list(objects)
        print(products_str)
        if (answer := input('Что выбираете?: ')).isdigit() and (
                answer := int(answer)) <= len(objects) + 1:
            if answer == len(objects) + 1:  # вернуться назад
                return None
            return objects[answer - 1]
        else:
            raise IncorrectAnswer('Неверный ответ')

    def feed_tamagochi(self) -> str:
        """Метод для кормления тамагочи"""
        if not self.storage_food:
            raise IsEmpty('В холодильнике пусто, сходите в магазин за едой')

        selected_food = self.choose_smth(self.storage_food)
        self.tamagochi.feed(selected_food)
        self.storage_food.remove(selected_food)
        return (f'Тамагочи съел {selected_food.name} и '
                f'восстановил {selected_food.satiety} единиц голода и энергии')

    def heal_tamagochi(self) -> str:
        """Метод для лечения тамагочи"""
        if not self.storage_medicine:
            raise IsEmpty('В аптечке пусто, сходите в магазин за лекарствами')

        selected_medicine = self.choose_smth(self.storage_medicine)
        self.tamagochi.heal(selected_medicine)
        selected_medicine.uses += 1
        if selected_medicine.is_empty():
            self.storage_medicine.remove(selected_medicine)
        return (f'Тамагочи принял {selected_medicine.name} и '
                f'восстановил {selected_medicine.heal_hp} единиц здоровья ')

    def rest_tamagochi(self) -> None:
        """Метод для отдыха тамагочи"""
        self.tamagochi.rest()

    def play_with_tamagochi(self) -> None:
        """Метод для игры с тамагочи"""
        self.tamagochi.play()

    def get_status(self) -> dict[str, Any]:
        """
        Метод для получения статуса (всех характеристик) тамагочи

        :return: словарь со всеми характеристиками тамагочи
        """
        return self.tamagochi.status

    def restart(self):
        """Метод для рестарта игры."""
        self.tamagochi.restart()

        self.storage_food.clear()
        self.storage_medicine.clear()
        self.first_time_on_work = True

    @staticmethod
    def get_options_from_list(objects) -> str:
        """Метод для получения списка для выбора."""
        return '\n'.join(
            f'{i + 1}. {objects[i]}'
            for i in range(len(objects))
        ) + f'\n{len(objects) + 1}. Вернуться назад'

    @property
    def work_coef(self) -> float:
        """Свойство для доступа к множителю заработанных монет."""
        if self.tamagochi.is_sick():
            return 0.5
        elif self.tamagochi.is_happy():
            return 1.5
        else:
            return 1.0

    @property
    def food(self) -> list[Food]:
        """
        Свойство для доступа к сумке с едой

        :return: список с имеющимися (купленными) объектами еды.
        """
        return self.storage_food


    @property
    def medicine(self) -> list[Medicine]:
        """
        Свойство для доступа к сумке с лекарствами

        :return: список с имеющимися (купленными) объектами лекарств.
        """
        return self.storage_medicine


