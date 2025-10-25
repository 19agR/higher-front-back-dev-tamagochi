import os

from game.exceptions import GameExit, NotEnoughMoney, IncorrectAnswer, \
    TamagochiIsGone
from game.models import Food, Medicine
from game.tamagochi import AbstractTamagochi, FirstTamagochi
from game.clicker import AbstractClicker, RandomSymbolsClicker
from game.game import AbstractGame, NormalGame


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def run_game_tick(output, game):
    print(output)

    print(f"Сумка с едой: {game.food}")
    print(f"Сумка с лекарствами: {game.medicine}")

    status = game.get_status()
    # print(
    #     f"\nСтатус: голод {status['hunger']}, здоровье {status['hp']}, "
    #     f"энергия {status['energy']}, монет {status['coins']}\n"
    # )
    if game.tamagochi.is_sick():
        print("=======Тамагочи болеет======")
        print("=======Отдых действует менее эффективно=======")
    print("1. Пойти на работу")
    print("2. Купить еду")
    print("3. Купить лекарство")
    print("4. Покормить")
    print("5. Вылечить")
    print("6. Играть")
    print("7. Отдых")
    print("0. Выход")

    match input("Выберите действие: "):
        case "1":
            income = game.work()
            output = (f'Вы вернулись с работы и заработали {income} монет.\n'
                      f'На вашем счету: {game.storage_money} монет')
            game.tamagochi.update()
        case "2":
            output = game.buy_food()
        case "3":
            output = game.buy_medicine()
        case "4":
            game.feed_tamagochi()
            output = ''
        case "5":
            game.heal_tamagochi()
            output = ''
        case "6":
            game.play_with_tamagochi()
            output = 'Вы поиграли с питомцем'
        case "7":
            game.rest_tamagochi()
            output = 'Питомец отдохнул'
        case "0":
            raise GameExit()
        case _:
            output = "Неверная команда"

    return output


def main():
    all_food = [
        Food(name='Бургер', satiety=20, price=40),
        Food(name='Салат', satiety=10, price=20),
        Food(name='Яблоко', satiety=10, price=15)
    ]

    all_medicine = [
        Medicine(name='Ибупрофен', price=30, heal_hp=20, number_of_uses=2)
    ]

    tamagochi = FirstTamagochi()
    clicker = RandomSymbolsClicker(income_per_click=10)
    game = NormalGame(
        tamagochi,
        clicker,
        all_food=all_food,
        all_medicine=all_medicine
    )

    print("Добро пожаловать в Тамагочи-кликер!")
    output = ''

    while True:
        try:
            output = run_game_tick(output, game)
        except NotEnoughMoney:
            print(f'Упс, кажется монеток на счету не хватило для оплаты...\n'
                  f'Монеток на счету: {game.storage_money}')
        except IncorrectAnswer:
            print(f'Упс, кажется нет такого варианта, попробуйте снова!')
        except TamagochiIsGone:
            print(f'О нет, Тамагочи умер! '
                  f'Но вы всегда можете попробовать снова! Нужно просто '
                  f'забыть эту оплошность и перезапустить игру ;)')
        except GameExit:
            print('До новых встреч! Тамагочи будет скучать =)')
            break

        clear_screen()


if __name__ == "__main__":
    main()
