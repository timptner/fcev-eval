#! /usr/bin/env python3

"""
Calculate durations by grouping values of a signal
"""

import pandas as pd

from fcev.__main__ import DATA_DIR

CLEANED_DATA = DATA_DIR / 'cleaned'

PROCESSED_DATA = DATA_DIR / 'processed'


def calculate_duration_of_strategies(filename: str) -> dict[str, float]:
    """Iterate over dataset to recognize periods of constant strategy and calculate total duration of these groups"""
    df = pd.read_csv(CLEANED_DATA / f'{filename}.csv')

    duration_list = {}
    last_index = 0
    for index, data in df.iterrows():
        strategy = data['Strategie [-]']

        if strategy not in duration_list.keys():
            duration_list[strategy] = []

        if index == len(df) - 1:
            # last iteration: leave iteration early to avoid IndexError
            duration = data['Zeit [s]'] - df['Zeit [s]'][last_index]
            duration_list[strategy].append(duration)  # add last period
            continue

        if strategy != df['Strategie [-]'][index + 1]:
            duration = data['Zeit [s]'] - df['Zeit [s]'][last_index]
            duration_list[strategy].append(duration)
            last_index = index + 1

    strategies = {
        1.0: 'RegBrakeFuCeOff',
        2.0: 'ElecDrive',
        3.0: 'RegBrakeFuCeOn',
        4.0: 'LoadShift',
        5.0: 'Boost',
        6.0: 'FuCeDrive',
    }

    durations = {}
    for key, value in strategies.items():
        if key in duration_list.keys():
            durations[value] = sum(duration_list[key])
        else:
            durations[value] = None

    print(f"Calculated duration of each strategy for simulation '{filename}'")
    return durations


def store_strategy_durations() -> None:
    """Store strategy durations for each simulation into single .csv-file"""
    series_list = []
    simulations = [file.stem for file in CLEANED_DATA.iterdir()]
    for simulation in simulations:
        durations = calculate_duration_of_strategies(simulation)
        s = pd.Series(durations)
        s['Simulation'] = simulation
        series_list.append(s)

    df = pd.concat(series_list, axis=1).transpose()
    df = df.reindex(columns=[df.columns[-1], *df.columns[:-1]])

    file = PROCESSED_DATA / 'durations_strategy.csv'
    if file.exists():
        raise FileExistsError(f"Please delete '{file.name}' before running this script.")

    df.to_csv(file, index=False)
    print(f"Created new file '{file.name}'.")


def main() -> None:
    """Main entry-point for script"""
    store_strategy_durations()


if __name__ == '__main__':
    main()
