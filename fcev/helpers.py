import numpy as np

from typing import Callable, Union


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


def select_item_interactively(items: Union[list[str], list[tuple[str, str]]], question: str) -> str:
    """Select an item via user input"""
    print(question)
    print("Please select an item from the following list.")
    digits = len(str(len(items)))
    for index in range(len(items)):
        item = items[index]
        if isinstance(item, tuple):
            key, value = item
            print(f" [{str(index).zfill(digits)}] {key} ({value})")
        else:
            print(f" [{str(index).zfill(digits)}] {item}")
    number = ask_user_for_number(len(items) - 1)
    if isinstance(item, tuple):
        value = items[number][0]
    else:
        value = items[number]
    return value


def select_func_interactively(options: list[tuple[str, Callable]]) -> Callable:
    """Select a callable from list of tuples via user input"""
    option_list = [option[0] for option in options]
    option = select_item_interactively(option_list, question="Which program do you want to execute?")
    index = option_list.index(option)
    name, func = options[index]
    return func


def get_signal_names(simulation, with_units=False) -> dict[str, Union[str, tuple[str, str]]]:
    """Return a list of available signals and their reference names"""
    signals = {}
    for key, value in simulation['data'].items():
        if key in signals.keys():
            raise KeyError("Duplicated signal found!")
        if with_units:
            signals[key] = (value.attrs['Name'], value.attrs['Unit'])
        else:
            signals[key] = value.attrs['Name']
    return signals


def get_index_from_value(data: np.ndarray, value: int) -> int:
    """Return index of the closest existing value from list"""
    return np.abs(data - value).argmin()


def delete_calculations(simulation) -> None:
    """Delete group from simulation data"""
    if 'calculated' not in simulation.keys():
        print("No calculations in this simulation found. Abort!")
        return
    del simulation['calculated']
