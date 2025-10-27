import os

from game.constants import (TEXT_STATUS, TEXT_SICK, TEXT_HAPPY, TEXT_ACTIONS,
    TEXT_BAGS, ALL_FOOD, ALL_MEDICINE, TEXT_TAMAGOCHI_DIE,
    TEXT_NOT_ENOUGH_MONEY, TEXT_INCORRECT_ANSWER, TEXT_GAME_EXIT,
    TEXT_RESTART_GAME, TEXT_GREETER, TEXT_AFTER_PLAY, TEXT_AFTER_REST,
    TEXT_AFTER_WORK)
from game.exceptions import (GameExit, NotEnoughMoney, IncorrectAnswer,
    TamagochiIsGone, IsEmpty)
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

    output += TEXT_BAGS.format(food=game.food, medicine=game.medicine)

    output += TEXT_STATUS.format(**game.get_status())
    if game.tamagochi.is_sick():
        output += TEXT_SICK
    elif game.tamagochi.is_happy():
        output += TEXT_HAPPY

    output += TEXT_ACTIONS

    print(output)

    match input("Выберите действие: "):
        case "1":
            output = TEXT_AFTER_WORK.format(
                income=game.work(),
                **game.get_status()
            )
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
            output = TEXT_AFTER_PLAY
        case "7":
            game.rest_tamagochi()
            output = TEXT_AFTER_REST
        case "0":
            raise GameExit()
        case _:
            output = TEXT_INCORRECT_ANSWER
    result = game.tamagochi.update()
    if result:
        if output:
            output += '\n\n'
        output += f'===========\n{result}\n=========='

    return output


def main():
    """Создание всего необходимого и запуск игры."""
    tamagochi = FirstTamagochi()
    clicker = RandomSymbolsClicker(income_per_click=15)
    game = NormalGame(
        tamagochi,
        clicker,
        all_food=ALL_FOOD,
        all_medicine=ALL_MEDICINE
    )

    output = TEXT_GREETER

    while True:
        try:
            output = run_game_tick(output, game)
        except NotEnoughMoney:
            output = TEXT_NOT_ENOUGH_MONEY.format(**game.get_status())
        except IncorrectAnswer:
            output = TEXT_INCORRECT_ANSWER
        except TamagochiIsGone:
            print(TEXT_TAMAGOCHI_DIE)
            answer = input('Хотите попробовать снова?:\n1) Да\n2) Нет').strip()
            if answer == '1':
                game.restart()
                output = TEXT_RESTART_GAME
            else:
                break
        except GameExit:
            print(TEXT_GAME_EXIT)
            break
        except IsEmpty as err:
            output = str(err)

        clear_screen()


if __name__ == "__main__":
    main()
