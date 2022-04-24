#! /usr/bin/env python3

"""
Script to convert .mat-file to .csv-file for further evaluation
"""

import numpy as np
import pandas as pd
import scipy.io

from fcev.__main__ import DATA_DIR

RAW_DATA_DIR = DATA_DIR / 'raw'

CLEANED_DATA_DIR = DATA_DIR / 'cleaned'

FILES = {
    'wltp_bat': ('DATA_WLTP_BAT_SOC50.mat', 'TIME_WLTP_BAT_SOC50.mat'),
    'wltp_sc': ('DATA_WLTP_SC_SOC50.mat', 'TIME_WLTP_SC_SOC50.mat'),
}

SIGNAL_NAMES = RAW_DATA_DIR / 'Var_List.txt'


def store_as_csv(raw_data: np.ndarray, raw_time: np.ndarray, signal_names: list[str], filename: str) -> None:
    """Combine data and time arrays and store as .csv-file"""
    df = pd.DataFrame(raw_data, columns=signal_names)
    s = pd.Series(raw_time.transpose()[0])
    df['Zeit [s]'] = s
    df = df.reindex(columns=[df.columns[-1], *df.columns[:-1]])

    file = DATA_DIR / 'cleaned' / f'{filename}.csv'
    if file.exists():
        raise FileExistsError(f"Please delete '{file.name}' before running this script.")
    df.to_csv(file, index=False)
    print(f"Created new file '{file.name}'.")


def convert_wltp_battery(data_file: str, time_file: str) -> None:
    """Convert .mat-file with simulation data from WLTP_BAT_SOC50"""
    raw_data = scipy.io.loadmat(RAW_DATA_DIR / data_file)
    raw_time = scipy.io.loadmat(RAW_DATA_DIR / time_file)

    signal_names = SIGNAL_NAMES.read_text().splitlines()
    signal_names.pop(signal_names.index('omega [rad/s]'))  # remove omega from list

    store_as_csv(raw_data['Data_WLTP_Bat'], raw_time['Time_WLTP_Bat'], signal_names, 'WLTP_BAT_SOC50')


def convert_wltp_supercap(data_file: str, time_file: str) -> None:
    """Convert .mat-file with simulation data from WLTP_SC_SOC50"""
    raw_data = scipy.io.loadmat(RAW_DATA_DIR / data_file)
    raw_time = scipy.io.loadmat(RAW_DATA_DIR / time_file)

    signal_names = SIGNAL_NAMES.read_text().splitlines()
    signal_names.pop(-1)  # remove last element to match data columns count

    store_as_csv(raw_data['Data_WLTP_SC'], raw_time['Time_WLTP_SC'], signal_names, 'WLTP_SC_SOC50')


def main() -> None:
    """Main entry-point for script"""
    convert_wltp_battery(*FILES['wltp_bat'])
    convert_wltp_supercap(*FILES['wltp_sc'])


if __name__ == '__main__':
    main()
