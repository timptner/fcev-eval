import h5py
import numpy as np

from datetime import datetime
from h5py._hl.group import Group as H5Group
from h5py._hl.dataset import Dataset as H5Dataset
from typing import Callable

import typer

from .helpers import select_item_interactively

app = typer.Typer()


def group_strategy(value: float) -> str:
    """Return group name decided from value"""
    groups = {
        1: "RegBrakeFuCeOn",
        2: "ElecDrive",
        3: "RegBrakeFuCeOff",
        4: "LoadShift",
        5: "Boost",
        6: "FuCeDrive",
    }
    return groups[int(value)]


def group_loading(value: float) -> str:
    """Return group name decided from value"""
    if value > 0:
        response = "Charge increasing"
    elif value < 0:
        response = "Charge depleting"
    elif value == 0:
        response = "Charge sustaining"
    else:
        typer.secho(f"Impossible value received: {value}")
        raise typer.Abort()
    return response


Duration = tuple[int, int]
Groups = dict[str, list[Duration]]


def create_index_list(data: np.ndarray, grouper: Callable[[float], str]) -> Groups:
    """Create a list of durations for each group"""
    groups = {}
    last_index = 0  # Use 0 as a start index for the first duration
    for index, value in enumerate(data):
        group = grouper(value)
        if group not in groups.keys():
            # Add list to avoid AttributeError when key does not exist
            groups[group] = []

        if index == len(data) - 1:
            # Last iteration: add missing last entry
            groups[group].append((last_index, index))
            continue

        if group != grouper(data[index + 1]):
            # Last index before group changes on next iteration
            groups[group].append((last_index, index))
            last_index = index + 1
    return groups


Durations = dict[str, int]


def convert_index_to_duration(groups: Groups, time: np.ndarray) -> Durations:
    """Convert indexes into timestamps and calculate duration for each distance"""
    durations = {}
    for key, duration in groups.items():
        duration_list = [time[end] - time[start] for start, end in duration]
        durations[key] = sum(duration_list)
    return durations


def store(simulation, signal: str, durations: Durations) -> None:
    """Save calculated durations to storage"""
    if 'calculated' not in simulation.keys():
        simulation.create_group('calculated')

    group = simulation['calculated']

    duration_list = [key for key in group.keys() if key.startswith('duration')]
    if duration_list:
        last_duration: str = max(duration_list)
        counter = int(last_duration.removesuffix('.png').removeprefix('duration')) + 1
        name = f'duration{counter:02d}'
    else:
        name = f'duration{1:02d}'

    duration = group.create_group(name)
    duration.attrs.create('Signal', signal)
    duration.attrs.create('Timestamp UTC', str(datetime.utcnow()))

    index = 1
    for key, value in durations.items():
        ds = duration.create_dataset(f'group{index:02d}', data=[value])
        ds.attrs.create('Name', key)
        ds.attrs.create('Unit', 's')
        index += 1


@app.command()
def calculate(ctx: typer.Context) -> None:
    """Calculate new duration and store results"""
    options = [
        (group_strategy, "Strategie"),
        (group_loading, "elektr. Gesamtleistung"),
    ]
    func_list, signal_list = zip(*options)

    file: h5py.File = ctx.obj

    simulations = [(value, value.attrs['Name']) for value in file.values()]
    simulation: H5Group = select_item_interactively(simulations, prompt="Available simulations")

    time = simulation['time'][:]

    signals = [(value, value.attrs['Name']) for value in simulation['data'].values() if value.attrs['Name'] in signal_list]
    signal: H5Dataset = select_item_interactively(signals, prompt="Available signals")

    options_index = signal_list.index(signal.attrs['Name'])
    func: Callable = func_list[options_index]

    groups = create_index_list(signal[:], func)
    durations = convert_index_to_duration(groups, time)
    typer.secho("Calculated durations for each set.", fg=typer.colors.GREEN)

    store(simulation, signal.attrs['Name'], durations)
    typer.secho("Durations were saved successfully.", fg=typer.colors.GREEN)

    show_results = typer.confirm("Show results?")
    if show_results:
        for key, value in durations.items():
            msg = typer.style(key, fg=typer.colors.CYAN)
            typer.echo(f'{msg}: {value} seconds')
        total = round(sum(durations.values()), 3)
        typer.echo(f"Total: {total} seconds")


@app.command()
def delete(ctx: typer.Context) -> None:
    """Delete group from simulation data"""
    file: h5py.File = ctx.obj

    simulations = [(value, value.attrs['Name']) for value in file.values()]
    simulation: H5Group = select_item_interactively(simulations, prompt="Available simulations")

    if 'calculated' not in simulation.keys():
        typer.secho("Simulation does not have any calculations.", fg=typer.colors.RED)
        raise typer.Abort()

    del simulation['calculated']
