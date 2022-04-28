#! /usr/bin/env python3

"""
Calculate durations by grouping values of a signal
"""

import numpy as np
import pandas as pd

from fcev.__main__ import DATA_DIR

PROCESSED_DATA = DATA_DIR / 'processed'

SIMULATIONS = [
    ('WLTP_BAT_SOC50', 1800),
    ('WLTP_SC_SOC50', 1800),
    ('Artemis130_BAT_SOC50', 1068),
    ('Artemis130_SC_SOC50', 1068),
    # ('ArtemisFull_BAT_SOC50', 4211),
    # ('ArtemisFull_SC_SOC50', 4211),
]


def select_strategy(value: float) -> str:
    """Return the strategy for the provided value"""
    if value == 1.0:
        return 'RegBrakeFuCeOff'
    elif value == 2.0:
        return 'ElecDrive'
    elif value == 3.0:
        return 'RegBrakeFuCeOn'
    elif value == 4.0:
        return 'LoadShift'
    elif value == 5.0:
        return 'Boost'
    elif value == 6.0:
        return 'FuCeDrive'
    else:
        raise ValueError("Unknown strategy")


def calculate_duration_of_strategies(df: pd.DataFrame, stop: int) -> pd.Series:
    """Iterate over dataset to recognize periods of constant strategy and calculate total duration of those groups"""
    if not stop < df['Zeit [s]'].max():
        raise ValueError("Stop-Attribute must be smaller than simulation time")

    strategies = ['RegBrakeFuCeOff', 'ElecDrive', 'RegBrakeFuCeOn', 'LoadShift', 'Boost', 'FuCeDrive']
    s = pd.Series(data=np.zeros(len(strategies)), index=strategies)

    last_index = 0
    for index, data in df.iterrows():
        strategy = select_strategy(data['Strategy'])

        if data['Zeit [s]'] > stop:
            # last iteration: leave iteration early to avoid IndexError
            duration = df['Zeit [s]'][index - 1] - df['Zeit [s]'][last_index]
            s[strategy] += duration  # add last period
            break

        if data['Strategy'] != df['Strategy'][index + 1]:
            duration = data['Zeit [s]'] - df['Zeit [s]'][last_index]
            s[strategy] += duration
            last_index = index

    return s


def store_strategy_durations(df: pd.DataFrame) -> None:
    """Store strategy durations for each simulation into single .csv-file"""
    file = PROCESSED_DATA / 'durations_strategy.csv'
    df.to_csv(file, index=False)
    print(f"Saved durations to file: {file.name}")


def main() -> None:
    """Main entry-point for script"""
    durations_list = []
    for simulation, duration in SIMULATIONS:
        df_data = pd.read_csv(DATA_DIR / 'raw' / f'{simulation}.csv')
        s = calculate_duration_of_strategies(df_data, stop=duration)
        s['Simulation'] = simulation
        durations_list.append(s)
        print(f"Calculated new duration: {simulation}")

    df = pd.concat(durations_list, axis=1).transpose()
    df = df.reindex(columns=['Simulation', *df.columns.drop('Simulation')])  # Set simulations column as first column
    store_strategy_durations(df)
    print("Done!")


if __name__ == '__main__':
    main()
