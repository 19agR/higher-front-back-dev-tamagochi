from string import ascii_uppercase

from game.models import Food, Medicine

"""Модуль со всеми константами"""

# настройки кликера:
INCOME_PER_CLICK = 10
SYMBOLS_FOR_CLICKER = ascii_uppercase

# настройки Тамагочи:
MAX_VALUE_FOR_FEATURE = 100
MIN_VALUE_FOR_FEATURE = 0
FEATURE_WITHOUT_MAX_VALUE = {'coins'}

# настройки игры:
TEXT_STATUS = (
    "\nСтатус: голод {hunger}%, здоровье {hp}%, "
    "энергия {energy}%, монет {coins:.0f}, "
    "счастье {happiness}%\n"
)
TEXT_BAGS = (
    "Сумка с едой: {food}\n"
    "Сумка с лекарствами: {medicine}\n"
)
TEXT_SICK = (
    "=======Тамагочи болеет======\n"
    "=======Отдых и работа действуют менее эффективно=======\n"
    "=======Необходимо дать Тамагочи лекарства для излечения=======\n"
)
TEXT_HAPPY = (
    "=======Тамагочи счастлив======\n"
    "=======Отдых и работа действуют более эффективно=======\n"
)
TEXT_ACTIONS = (
    "1. Пойти на работу\n"
    "2. Купить еду\n"
    "3. Купить лекарство\n"
    "4. Покормить\n"
    "5. Вылечить\n"
    "6. Играть\n"
    "7. Отдых\n"
    "0. Выход\n"
)
TEXT_TAMAGOCHI_DIE = (
    'О нет, Тамагочи умер! '
    'Но вы всегда можете попробовать снова! Нужно просто '
    'забыть эту оплошность и перезапустить игру ;)'
)
TEXT_NOT_ENOUGH_MONEY = (
    'Упс, кажется монеток на счету не хватило для оплаты!\n'
    'Монеток на счету: {coins:.0f}'
)
TEXT_INCORRECT_ANSWER = 'Упс, кажется нет такого варианта, попробуйте снова!'
TEXT_GAME_EXIT = 'До новых встреч! Тамагочи будет скучать =)'
TEXT_RESTART_GAME = ('И снова добро пожаловать в Тамагочи-кликер!'
                     ' Попробуем еще раз =)')
TEXT_GREETER = 'Добро пожаловать в Тамагочи-кликер!'
TEXT_AFTER_WORK = (
    'Вы вернулись с работы и заработали '
    '{income:.0f} монет.\nНа вашем счету: {coins:.0f} монет'
)
TEXT_AFTER_PLAY = 'Вы немного поиграли с Тамагочи, и он стал счастливее =)'
TEXT_AFTER_REST = 'Тамагочи хорошенько отдохнул'
# стартовые настройки магазина:
ALL_FOOD = [
    Food(name='Бургер', satiety=50, price=40),
    Food(name='Салат', satiety=30, price=20),
    Food(name='Яблоко', satiety=10, price=5),
]

ALL_MEDICINE = [
    Medicine(name='Ибупрофен', price=30, heal_hp=25, number_of_uses=2),
    Medicine(name='Омез', price=50, heal_hp=40, number_of_uses=2)
]
