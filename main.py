import os

from game.exceptions import (GameExit, NotEnoughMoney, IncorrectAnswer,
    TamagochiIsGone, IsEmpty)
from game.models import Food, Medicine
from game.tamagochi import FirstTamagochi
from game.clicker import RandomSymbolsClicker
from game.game import NormalGame


def clear_screen():
    """Очищает экран."""
    os.system('cls' if os.name == 'nt' else 'clear')


def run_game_tick(output, game):
    """Все действия в рамках одного хода."""
    if output:
        output += '\n\n'

    output += (f"Сумка с едой: {game.food}\n"
               f"Сумка с лекарствами: {game.medicine}\n")

    status = game.get_status()
    output += (
        f"\nСтатус: голод {status['hunger']}%, здоровье {status['hp']}%, "
        f"энергия {status['energy']}%, монет {status['coins']:.0f}, "
        f"счастье {status['happiness']}%\n"
    )
    if game.tamagochi.is_sick():
        output += (
            "=======Тамагочи болеет======\n"
            "=======Отдых и работа действуют менее эффективно=======\n"
            "=======Необходимо дать Тамагочи лекарства для излечения=======\n"
        )
    elif game.tamagochi.is_happy():
        output += (
            "=======Тамагочи счастлив======\n"
            "=======Отдых и работа действуют более эффективно=======\n"
        )

    output += (
        "1. Пойти на работу\n"
        "2. Купить еду\n"
        "3. Купить лекарство\n"
        "4. Покормить\n"
        "5. Вылечить\n"
        "6. Играть\n"
        "7. Отдых\n"
        "0. Выход\n"
    )

    print(output)

    match input("Выберите действие: "):
        case "1":
            income = game.work()
            output = (f'Вы вернулись с работы и заработали '
                      f'{income:.0f} монет.\nНа вашем счету: '
                      f'{game.tamagochi.status["coins"]:.0f} монет')
        case "2":
            output = game.buy_food()
        case "3":
            output = game.buy_medicine()
        case "4":
            output = game.feed_tamagochi()
        case "5":
            output = game.heal_tamagochi()
        case "6":
            game.play_with_tamagochi()
            output = 'Вы немного поиграли с Тамагочи, и он стал счастливее =)'
        case "7":
            game.rest_tamagochi()
            output = 'Тамагочи хорошенько отдохнул'
        case "0":
            raise GameExit()
        case _:
            output = "Неверная команда"
    result = game.tamagochi.update()
    if result:
        if output:
            output += '\n\n'
        output += f'===========\n{result}\n=========='

    return output


def main():
    """Создание всего необходимого и запуск игры."""
    all_food = [
        Food(name='Бургер', satiety=50, price=40),
        Food(name='Салат', satiety=30, price=20),
        Food(name='Яблоко', satiety=10, price=5),
    ]

    all_medicine = [
        Medicine(name='Ибупрофен', price=30, heal_hp=25, number_of_uses=2),
        Medicine(name='Омез', price=50, heal_hp=40, number_of_uses=2)
    ]

    tamagochi = FirstTamagochi()
    clicker = RandomSymbolsClicker(income_per_click=15)
    game = NormalGame(
        tamagochi,
        clicker,
        all_food=all_food,
        all_medicine=all_medicine
    )

    output = 'Добро пожаловать в Тамагочи-кликер!'

    while True:
        try:
            output = run_game_tick(output, game)
        except NotEnoughMoney:
            output = ('Упс, кажется монеток на счету не хватило для оплаты!\n'
                      'Монеток на счету: '
                      f'{game.tamagochi.status["coins"]:.0f}')
        except IncorrectAnswer:
            output = 'Упс, кажется нет такого варианта, попробуйте снова!'
        except TamagochiIsGone:
            print('О нет, Тамагочи умер! '
                  'Но вы всегда можете попробовать снова! Нужно просто '
                  'забыть эту оплошность и перезапустить игру ;)')
            answer = input('Хотите попробовать снова?:\n1) Да\n2) Нет').strip()
            if answer == '1':
                game.restart()
                output = ('И снова добро пожаловать в Тамагочи-кликер! '
                          'Попробуем еще раз =)')
            else:
                break
        except GameExit:
            print('До новых встреч! Тамагочи будет скучать =)')
            break
        except IsEmpty as err:
            output = str(err)

        clear_screen()


if __name__ == "__main__":
    main()
