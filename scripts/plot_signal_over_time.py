#! /usr/bin/env python3

"""
Plot selected signals over time and save image file to disk.
"""

import matplotlib.pyplot as plt
import pandas as pd
import re

from fcev.__main__ import BASE_DIR, DATA_DIR
from fcev.helpers import mm2inch
from typing import Optional

IMAGE_DIR = BASE_DIR / 'figures' / 'signal_over_time'

SIMULATIONS = [
    'WLTP_BAT_SOC50',
    'WLTP_SC_SOC50',
    'Artemis130_BAT_SOC50',
    'Artemis130_SC_SOC50',
    # 'ArtemisFull_BAT_SOC50',
    # 'ArtemisFull_SC_SOC50',
]

SIGNALS = [
    ('levelH2 [-]', "Tankpegel H2"),
    ('SOC [-]', "Ladezustand"),
    ('Strategy', "Strategie"),
    ('v [m/s]', "Geschwindigkeit Fahrzeug"),
    ('vSet [m/s]', "Geschwindigkeit Fahrzyklus"),
]

Signal = tuple[str, Optional[str]]


def split_name_and_unit(signal: str) -> Signal:
    """Return the name and unit for a signal seperated"""
    result = re.match(r'^(\w+)(\s\[([\w\-/]+)\])?$', signal)
    if result:
        name = result.group(1)
        unit = result.group(3)
    else:
        name = signal
        unit = None
    return name, unit


def main() -> None:
    """Main entry-point for script"""
    if not IMAGE_DIR.exists():
        IMAGE_DIR.mkdir(parents=True)

    for simulation in SIMULATIONS:
        df = pd.read_csv(DATA_DIR / 'raw' / f'{simulation}.csv')

        for signal, label in SIGNALS:
            name, unit = split_name_and_unit(signal)

            fig, ax = plt.subplots(figsize=(mm2inch(150), mm2inch(100)), dpi=300, layout='constrained')

            ax.plot(df['Zeit [s]'], df[signal])

            ax.grid(visible=True)
            ax.set_xlabel('Zeit [s]')
            ax.set_ylabel(f"{label} [{unit}]" if unit else label)

            filename = f'{simulation}_{name}'
            fig.savefig(IMAGE_DIR / f'{filename}.png')

            print(f"Saved a new figure: {filename}")

    print("Done!")


if __name__ == '__main__':
    main()
