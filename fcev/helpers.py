import numpy as np
import typer

from pathlib import Path
from typing import Union, Any


def ask_user_for_number(limit: int, prompt: str = None) -> int:
    """Prompt for a number and validate the response"""
    while True:
        response = typer.prompt(prompt or "Select a number")
        try:
            index = int(response)
        except ValueError:
            typer.secho(f"Not a number. Try again!", fg=typer.colors.RED)
            continue
        if index not in range(limit + 1):
            typer.secho(f"Number must be between 0 and {limit}. Try again!", fg=typer.colors.RED)
            continue
        return index


def select_item_interactively(items: Union[list[str], list[tuple[str, str]]], prompt: str) -> Any:
    """Select an item via user input"""
    message = typer.style(f"--- {prompt} ---", fg=typer.colors.BLUE, bold=True)
    typer.echo(message)

    digits = len(str(len(items)))
    for index, item in enumerate(items):
        msg_index = typer.style(f" {str(index).zfill(digits)} ", bg=typer.colors.BLUE)
        if isinstance(item, tuple):
            typer.echo(f"{msg_index} {item[1]}")
        else:
            typer.echo(f"{msg_index} {item}")

    number = ask_user_for_number(len(items) - 1)
    if isinstance(items[number], tuple):
        value = items[number][0]
    else:
        value = items[number]
    return value


def get_unique_image_name(path: Path, name: str) -> Path:
    """Return valid path with unique filename"""
    if not path.exists():
        path.mkdir()
        typer.echo("Images directory created!")

    images = [file.stem for file in path.iterdir() if file.suffix == '.png']
    numbers = [int(image.removesuffix('.png').removeprefix(name)) for image in images if image.startswith(name)]
    if numbers:
        number = max(numbers) + 1
    else:
        number = 1

    file_path = path / f'{name}{number:03d}.png'
    if file_path.exists():
        raise FileExistsError("File already exists. Please execute again to generate new unique name.")
    return file_path


def get_key_by_attribute(group: dict, key: str, value: str) -> list[str]:
    """Query group items by attribute and return result"""
    return [key_ for key_, value_ in group.items() if value_.attrs[key] == value]


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


def mm2inch(value: Union[int, float]) -> float:
    """Return inches from millimeters round by 2 digits"""
    return round(value / 25.4, 2)
