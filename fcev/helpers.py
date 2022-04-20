from typing import Callable


def ask_user_for_number(max_int: int) -> int:
    print("Choose a number:")
    while True:
        response = input("> ")
        try:
            index = int(response)
        except ValueError:
            print("Not a number. Try again!")
            continue
        if index not in range(max_int + 1):
            print(f"Only numbers between 0 and {max_int} are valid. Try again!")
            continue
        return index


def select_item_interactively(items: list[str], question: str) -> str:
    """Select a list item via user input"""
    print(question)
    print("Please select an item from the following list.")
    digits = len(str(len(items)))
    for index in range(len(items)):
        print(f" [{str(index).zfill(digits)}] {items[index]}")
    index = ask_user_for_number(len(items) - 1)
    value = items[index]
    return value


def select_func_interactively(options: list[tuple[str, callable]]) -> callable:
    """Select a callable from list of tuples via user input"""
    option_list = [option[0] for option in options]
    option = select_item_interactively(option_list, question="Which program do you want to execute?")
    index = option_list.index(option)
    name, func = options[index]
    return func
