#! /usr/bin/env python3

from pathlib import Path

import h5py

from .duration import calculate as calc_duration
from .plotter import plot_signal, plot_duration
from .helpers import select_func_interactively, select_item_interactively, delete_calculations, ask_user_for_number

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / 'data'


def main() -> None:
    """Main entry-point for script"""
    options = [
        ("Plot signal over time", plot_signal),
        ("Calculate duration of a signal", calc_duration),
        ("Plot duration as pie chart", plot_duration),
        ("Delete calculations", delete_calculations),
    ]
    func = select_func_interactively(options)
    with h5py.File(DATA_DIR / 'simulation.hdf5', 'r+') as file:
        sim_list = [(key, value.attrs['Name']) for key, value in file.items()]
        group = select_item_interactively(sim_list, question="Which simulation do you want to evaluate?")
        simulation = file[group]
        func(simulation)


if __name__ == '__main__':
    main()
