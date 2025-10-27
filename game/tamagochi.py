"""Модуль с интерфейсом и реализациями класса Тамагочи"""

from abc import ABC, abstractmethod

from .constants import (MAX_VALUE_FOR_FEATURE, MIN_VALUE_FOR_FEATURE,
    FEATURE_WITHOUT_MAX_VALUE)
from .exceptions import TamagochiIsGone
from .models import Food, Medicine


class AbstractTamagochi(ABC):
    """Интерфейс логики Тамагочи."""

    @abstractmethod
    def feed(self, food: Food) -> None:
        """
        Абстрактный метод для кормления Тамагочи

        :param food: объект еды для кормления.
        """
        raise NotImplementedError

    @abstractmethod
    def play(self) -> None:
        """Абстрактный метод для игры с Тамагочи."""
        raise NotImplementedError

    @abstractmethod
    def rest(self) -> None:
        """Абстрактный метод для отдыха Тамагочи."""
        raise NotImplementedError

    @abstractmethod
    def heal(self, medicine: Medicine) -> None:
        """
        Абстрактный метод для лечения Тамагочи

        :param medicine: лекарство для лечения.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def status(self) -> dict[str, int]:
        """
        Абстрактное свойство для доступа ко всем состояниям Тамагочи

        :return: словарь со всеми состояниями Тамагочи.
        """
        raise NotImplementedError

    @abstractmethod
    def is_alive(self) -> bool:
        """
        Абстрактный метод для проверки жив ли Тамагочи

        :return: True если жив, иначе False.
        """
        raise NotImplementedError

    @abstractmethod
    def is_sick(self) -> bool:
        """
        Абстрактный метод для проверки, не заболел ли Тамагочи

        :return: True если Тамагочи болеет, иначе False.
        """
        raise NotImplementedError

    @abstractmethod
    def update(self) -> None:
        """
        Абстрактный метод для обновления состояний Тамагочи.
        Должен использоваться после каждого взаимодействия с Тамагочи.
        """
        raise NotImplementedError

    @abstractmethod
    def change_feature(self, feature, amount) -> None:
        """Абстрактный метод для изменения свойств Тамагочи."""
        raise NotImplementedError

    @abstractmethod
    def work(self) -> None:
        """Абстрактный метод для изменения свойств Тамагочи."""
        raise NotImplementedError

    @abstractmethod
    def is_happy(self) -> bool:
        """
        Абстрактный метод для проверки, счастлив ли Тамагочи

        :return: True если Тамагочи счастлив, иначе False.
        """
        raise NotImplementedError

    @abstractmethod
    def restart(self) -> None:
        """Абстрактный метод для сброса всех свойств до базовых настроек."""
        raise NotImplementedError


class FirstTamagochi(AbstractTamagochi):
    """Интерфейс логики Тамагочи."""

    def __init__(self):
        """Создание констант для изменения свойств Тамагочи."""
        self.restart()
        self._hunger_increase_for_action = 5
        self._energy_decrease_for_action = -5
        self._energy_increase_for_action = 15
        self._hp_decrease_for_action = -5
        self._hp_increase_for_action = 5
        self._happiness_increase_for_action = 25
        self._happiness_decrease_for_action = -25
        self._need_hp_for_sick = 40
        self._need_happiness_for_happy = 80
        self._food_give_energy_coef = 0.5

        self._lvl_of_energy_to_decrease_hp = 20
        self._lvl_of_hunger_to_decrease_hp = 80
        self._lvl_of_happiness_to_decrease_hp = 25


    def work(self):
        """Метод для изменения свойств Тамагочи."""

    def feed(self, food: Food) -> None:
        """
        Метод для кормления Тамагочи

        :param food: объект еды для кормления
        """
        self.change_feature('hunger', -food.satiety)
        self.change_feature('energy',
                            int(food.satiety * self._food_give_energy_coef))

    def play(self) -> None:
        """Метод для игры с Тамагочи"""
        self.change_feature('happiness', self._happiness_increase_for_action)
        self.change_feature('hp', self._hp_increase_for_action)
        self.change_feature('energy', self._energy_decrease_for_action)

    def rest(self) -> None:
        """Метод для отдыха Тамагочи"""
        self.change_feature('energy', self._energy_increase_for_action)
        self.change_feature('hunger', self._hunger_increase_for_action)

    def heal(self, medicine: Medicine) -> None:
        """
        Метод для лечения Тамагочи

        :param medicine: лекарство для лечения
        """
        self.change_feature('hp', medicine.heal_hp)
        self._status['sick'] = False

    def change_feature(self, feature: str, amount: int) -> None:
        """Метод для изменения свойств Тамагочи."""
        self._status[feature] += amount
        if (self._status[feature] > MAX_VALUE_FOR_FEATURE
                and feature not in FEATURE_WITHOUT_MAX_VALUE):
            self._status[feature] = MAX_VALUE_FOR_FEATURE
        elif self._status[feature] < MIN_VALUE_FOR_FEATURE:
            self._status[feature] = MIN_VALUE_FOR_FEATURE

    @property
    def status(self) -> dict[str, int]:
        """
        Свойство для доступа ко всем состояниям Тамагочи

        :return: словарь со всеми состояниями Тамагочи.
        """
        return self._status

    def is_alive(self) -> bool:
        """
        Метод для проверки жив ли Тамагочи

        :return: True если жив, иначе False.
        """
        return self._status['alive']

    def is_sick(self) -> bool:
        """
        Метод для проверки, не заболел ли Тамагочи

        :return: True если Тамагочи болеет, иначе False.
        """
        return self._status['sick']

    def is_happy(self):
        """
        Метод для проверки, счастлив ли Тамагочи

        :return: True если Тамагочи счастлив, иначе False.
        """
        return self._status['happiness'] >= self._need_happiness_for_happy

    def update(self) -> str:
        """
        Метод для обновления состояний Тамагочи.
        Должен использоваться после каждого взаимодействия с Тамагочи.
        """
        output = ''
        need_decrease_hp = False
        need_decrease_happiness = False

        self.change_feature('hunger', self._hunger_increase_for_action)
        self.change_feature('energy', self._energy_decrease_for_action)

        if self._status['energy'] <= self._lvl_of_energy_to_decrease_hp:
            need_decrease_hp = need_decrease_happiness = True
            output += ('\nВнимание! Низкий запас энергии, снижается здоровье.'
                       ' Дайте Тамагочи лекарство')

        if self._status['hunger'] >= self._lvl_of_hunger_to_decrease_hp:
            need_decrease_hp = need_decrease_happiness = True
            output += ('\nВнимание! Низкий запас голода, снижается здоровье.'
                       ' Покормите Тамагочи')

        if self._status['happiness'] <= self._lvl_of_happiness_to_decrease_hp:
            need_decrease_hp = True
            output += ('\nВнимание! Низкий запас счастья, риск депрессии '
                       'снижается здоровье. Поиграйте с Тамагочи')

        if need_decrease_hp:
            self.change_feature('hp', self._hp_decrease_for_action)
        if need_decrease_happiness:
            self.change_feature('happiness',
                                self._happiness_decrease_for_action)

        if self._status['hp'] == 0:
            self._status['alive'] = False
        elif self._status['hp'] <= self._need_hp_for_sick:
            self._status['sick'] = True
            output += ('\nВнимание! Из-за низкого уровня здоровья'
                       ' Тамагочи заболел. Дайте Тамагочи лекарство, а также'
                       ' проверьте параметры голода и энергии')

        if not self.is_alive():
            raise TamagochiIsGone('Тамагочи умер =(')

        return output.lstrip()

    def restart(self):
        """Метод для сброса всех свойств до базовых настроек."""
        self._status = {
            'alive': True,
            'sick': False,
            'hp': 100,
            'energy': 100,
            'hunger': 0,
            'happiness': 50,
            'coins': 0
        }


