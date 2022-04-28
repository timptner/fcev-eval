#! /usr/bin/env python3

"""
Calculate durations by grouping values of a signal
"""

import numpy as np
import pandas as pd

from fcev.__main__ import DATA_DIR
from typing import Callable

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
        return "RegBrakeFuCeOff"
    elif value == 2.0:
        return "ElecDrive"
    elif value == 3.0:
        return "RegBrakeFuCeOn"
    elif value == 4.0:
        return "LoadShift"
    elif value == 5.0:
        return "Boost"
    elif value == 6.0:
        return "FuCeDrive"
    else:
        raise ValueError("Unknown strategy")


def select_charging(value: float) -> str:
    """Return the charging behaviour for the provided value"""
    if value == 0:
        return "Charge sustaining"
    elif value > 0:
        return "Charge increasing"
    elif value < 0:
        return "Charge depleting"
    else:
        raise ValueError("Unknown charging behaviour")


SelectFunc = Callable[[float], str]


def calculate_duration(df: pd.DataFrame, column: str, groups: list[str],
                       select_func: SelectFunc, stop: int) -> pd.Series:
    """Iterate over dataset to recognize periods of consistent behaviour and calculate total duration of those groups"""
    if not stop < df['Zeit [s]'].max():
        raise ValueError("Stop-Attribute must be smaller than simulation time")

    s = pd.Series(data=np.zeros(len(groups)), index=groups)

    last_index = 0
    for index, data in df.iterrows():
        group = select_func(data[column])

        if data['Zeit [s]'] > stop:
            # last iteration: leave iteration early to avoid IndexError
            duration = df['Zeit [s]'][index - 1] - df['Zeit [s]'][last_index]
            s[group] += duration  # add last period
            break

        if data[column] != df[column][index + 1]:
            duration = data['Zeit [s]'] - df['Zeit [s]'][last_index]
            s[group] += duration
            last_index = index

    return s


def store_durations(durations: list[pd.Series], name: str) -> None:
    """Store durations for each simulation into single .csv-file"""
    df = pd.concat(durations, axis=1).transpose()
    df = df.reindex(columns=['Simulation', *df.columns.drop('Simulation')])

    file = PROCESSED_DATA / f'durations_{name}.csv'
    df.to_csv(file, index=False)
    print(f"Saved durations to file: {file.name}")


def main() -> None:
    """Main entry-point for script"""
    strategy_durations = []
    charging_durations = []

    for simulation, duration in SIMULATIONS:
        df_data = pd.read_csv(DATA_DIR / 'raw' / f'{simulation}.csv')

        # Strategies
        groups = ['RegBrakeFuCeOff', 'ElecDrive', 'RegBrakeFuCeOn', 'LoadShift', 'Boost', 'FuCeDrive']
        s_strategy = calculate_duration(df_data, column='Strategy', groups=groups,
                                        select_func=select_strategy, stop=duration)
        s_strategy['Simulation'] = simulation
        strategy_durations.append(s_strategy)
        print(f"Calculated new strategy durations: {simulation}")

        # Charging
        groups = ['Charge increasing', 'Charge depleting', 'Charge sustaining']
        s_charging = calculate_duration(df_data, column='Pel [W]', groups=groups,
                                        select_func=select_charging, stop=duration)
        s_charging['Simulation'] = simulation
        charging_durations.append(s_charging)
        print(f"Calculated new charging durations: {simulation}")

    store_durations(strategy_durations, 'strategy')
    store_durations(charging_durations, 'charging')

    print("Done!")


if __name__ == '__main__':
    main()
