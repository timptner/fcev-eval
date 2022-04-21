#! /usr/bin/env python3

from pathlib import Path

import h5py

from .duration import calculate as calc_duration
from .plotter import plot_signal
from .helpers import select_func_interactively, select_item_interactively

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / 'data'


def main() -> None:
    """Main entry-point for script"""
    options = [
        ("Calculate duration of a signal", calc_duration),
        ("Plot signal over time", plot_signal),
    ]
    func = select_func_interactively(options)
    with h5py.File(DATA_DIR / 'simulation.hdf5', 'r+') as file:
        group = select_item_interactively(list(file.keys()), question="Which simulation do you want to evaluate?")
        simulation = file[group]
        func(simulation)


if __name__ == '__main__':
    main()
