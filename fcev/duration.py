import numpy as np

from datetime import datetime
from typing import Callable

from .helpers import select_item_interactively


def get_item_by_attribute(group: dict, key: str, value: str) -> np.ndarray:
    """Query group items by attribute and return result"""
    signals = [dataset for dataset in group if dataset.attrs[key] == value]
    if len(signals) > 1:
        raise NotImplementedError("More than one signal found.")
    return signals[0][:]


Distance = tuple[int, int]
Result = dict[str, list[Distance]]


def create_grouped_index_list(data: np.ndarray, grouper: Callable[[float], str]) -> Result:
    """Create an index list for each defined group"""
    result = {}
    last_index = 0
    for index in range(len(data)):
        group = grouper(data[index])
        if group not in result.keys():
            # add list to avoid AttributeError when key does not exist
            result[group] = []
        if index == len(data) - 1:
            # last iteration: add missing last entry
            result[group].append((last_index, index))
            continue
        if group != grouper(data[index + 1]):
            result[group].append((last_index, index))
            last_index = index + 1
    return result


Durations = dict[str, int]


def calculate_durations(result: Result, time: np.ndarray) -> Durations:
    """Convert indexes into timestamps and calculate duration for each distance"""
    durations = {}
    for key, indexes in result.items():
        durations[key] = round(sum([time[end] - time[start] for start, end in indexes]), 3)
    return durations


def group_strategy(value: float) -> str:
    """Return group name decided from value"""
    groups = {
        1: "Rekuperation ohne Brennstoffzelle",
        2: "Elektrisches Fahren",
        3: "Rekuperation mit Brennstoffzelle",
        4: "Lastpunktverschiebung",
        5: "Verstärken",
        6: "Fahren mit Brennstoffzelle",
    }
    return groups[int(value)]


def group_loading(value: float) -> str:
    """Return group name decided from value"""
    if value > 0:
        response = "Laden"
    elif value < 0:
        response = "Entladen"
    elif value == 0:
        response = "Halten"
    else:
        response = "Unbekannte Verhalten!"
    return response


def store(simulation, signal: str, durations: Durations) -> None:
    """Save data into hdf5-file"""
    if 'calculated' not in simulation.keys():
        simulation.create_group('calculated')
    group = simulation['calculated']
    duration_list = [key for key in group.keys() if key.startswith('duration_')]
    if duration_list:
        last_duration = max(duration_list)
        index = int(last_duration.split('_')[-1]) + 1
        name = f'duration_{index:02d}'
    else:
        name = f'duration_{1:02d}'
    subgroup = group.create_group(name)
    subgroup.attrs.create('Signal', signal)
    subgroup.attrs.create('Timestamp UTC', str(datetime.utcnow()))
    index = 1
    for key, value in durations.items():
        ds = subgroup.create_dataset(f'set_{index:02d}', data=[value])
        ds.attrs.create('Name', key)
        ds.attrs.create('Unit', 's')
        index += 1


def calculate(simulation) -> None:
    """Main entry-point for script"""
    options = [
        ("Strategie", group_strategy),
        ("elektr. Gesamtleistung", group_loading),
    ]
    option_list = [option[0] for option in options]
    signal = select_item_interactively(option_list, question="Which signal do you want to calculate the duration for?")
    index = option_list.index(signal)
    func = options[index][1]

    data = get_item_by_attribute(simulation['data'].values(), 'Name', signal)
    result = create_grouped_index_list(data, func)
    time = simulation['time'][:]
    durations = calculate_durations(result, time)
    store(simulation, signal, durations)
    for key, value in durations.items():
        print(f'{key}: {value}s')
    print(f"Total: {round(sum(durations.values()), 3)}")
