#! /usr/bin/env python3

import h5py
import re
import scipy.io

from pathlib import Path
from typing import List, Tuple, Optional

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / 'data'

FILES = [
    'DATA_WLTP_BAT_SOC50.mat',
    'TIME_WLTP_BAT_SOC50.mat',
    'DATA_WLTP_SC_SOC50.mat',
    'TIME_WLTP_SC_SOC50.mat',
]

HDF5_FILE = DATA_DIR / 'simulation.hdf5'


def convert_mat_to_hdf5():
    """Convert .mat file to .hdf5 file"""
    source = BASE_DIR / 'data/DATA_WLTP_BAT_SOC50.mat'
    data = scipy.io.loadmat(str(source))['Data_WLTP_Bat'].transpose()
    destination = BASE_DIR / 'data/wltp_bat_soc50.hdf5'
    signal_names = (BASE_DIR / 'data/Var_List.txt').read_text().splitlines()
    with h5py.File(destination, 'w') as f:
        group = f.create_group('data')
        for i in range(len(data)):
            dataset = group.create_dataset(str(i), data=data[i])
            dataset.attrs.create('Name', signal_names[i])


def get_public_key(keys: List[str]) -> str:
    """Return the public key from a list of public and private keys"""
    keys = [key for key in keys if not key.startswith('__')]
    if len(keys) > 1:
        raise NotImplementedError("More than 1 valid datasets found.")
    return keys[0]


def create_new_key(keys: List[str]) -> str:
    """Return new key with incremented index"""
    name = 'simulation_'
    cleaned_keys = [key for key in keys if key.startswith(name)]
    if cleaned_keys:
        last_key = max([int(key.replace(name, '')) for key in cleaned_keys])
    else:
        last_key = 0
    return f'{name}{last_key + 1:02d}'


def split_signal_into_name_and_unit(signal: str) -> Optional[Tuple[str]]:
    """Split signal into its name and unit"""
    result = re.match(r'^(.+)\s\[(.+)\]$', signal)
    if not result:
        return None
    return result.groups()


def load_mat_file(name: str):
    """Load .mat file from data dir"""
    source = DATA_DIR / name
    mat = scipy.io.loadmat(str(source))
    key = get_public_key(mat.keys())
    data = mat[key].transpose()
    return data


def write_signal_data_to_hdf5(name: str, signals: List[str]) -> str:
    """Load signal data from .mat-file to .hdf5-file and return used key"""
    data = load_mat_file(name)
    with h5py.File(HDF5_FILE, 'a') as file:
        key = create_new_key(file.keys())
        group = file.create_group(key)
        group.attrs.create('Name', name.removeprefix('DATA_').removesuffix('.mat'))
        subgroup = group.create_group('data')
        for i in range(len(data)):
            dataset = subgroup.create_dataset(f'signal_{i+1:02d}', data=data[i])
            try:
                name, unit = split_signal_into_name_and_unit(signals[i])
            except TypeError:
                name = signals[i]
                unit = ''
            dataset.attrs.create('Name', name)
            dataset.attrs.create('Unit', unit)
    return key


def write_time_data_to_hdf5(name: str, key: str):
    """Load time data from .mat-file to .hdf5-file"""
    data = load_mat_file(name)[0]
    with h5py.File(HDF5_FILE, 'r+') as file:
        group = file.get(key)
        if not group:
            raise KeyError("Simulation not found")
        dataset = group.create_dataset('time', data=data)
        dataset.attrs.create('Name', "Zeit")
        dataset.attrs.create('Unit', 's')


def main() -> None:
    """Main entry-point for script"""
    signals = (DATA_DIR / 'Var_List.txt').read_text().splitlines()
    key = write_signal_data_to_hdf5(FILES[2], signals)
    write_time_data_to_hdf5(FILES[3], key)
    signals.pop(8)  # remove 'omega' for battery
    key = write_signal_data_to_hdf5(FILES[0], signals)
    write_time_data_to_hdf5(FILES[1], key)


if __name__ == '__main__':
    main()
