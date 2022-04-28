#! /usr/bin/env python3

"""
Plot vehicle velocity and driving cycle velocity into a single subplot.
Also plot the flaw between both of them into another subplot.
Lastly store the plot onto disk.
"""

import matplotlib.pyplot as plt
import pandas as pd

from fcev.__main__ import BASE_DIR, DATA_DIR
from fcev.helpers import mm2inch

IMAGE_DIR = BASE_DIR / 'figures' / 'velocity_flaw'

SIMULATIONS = [
    'WLTP_BAT_SOC50',
    'WLTP_SC_SOC50',
    'Artemis130_BAT_SOC50',
    'Artemis130_SC_SOC50',
    # 'ArtemisFull_BAT_SOC50',
    # 'ArtemisFull_SC_SOC50',
]


def main() -> None:
    """Main entry-point for script"""
    if not IMAGE_DIR.exists():
        IMAGE_DIR.mkdir(parents=True)

    for simulation in SIMULATIONS:
        df = pd.read_csv(DATA_DIR / 'raw' / f'{simulation}.csv')

        fig, axs = plt.subplots(nrows=2, figsize=(mm2inch(150), mm2inch(100)), dpi=300, layout='constrained')

        # Both velocity signals
        axs[0].plot(df['Zeit [s]'], df['vSet [m/s]'], alpha=0.5, label='Fahrzyklus')
        axs[0].plot(df['Zeit [s]'], df['v [m/s]'], alpha=0.5, label='Fahrzeug')

        axs[0].grid(visible=True)
        axs[0].legend()
        axs[0].set_xlabel('Zeit [s]')
        axs[0].set_ylabel('Geschwindigkeit [m/s]')

        # Flaw of velocities
        flaw = df['v [m/s]'] - df['vSet [m/s]']
        axs[1].plot(df['Zeit [s]'], flaw)

        axs[1].grid(visible=True)
        axs[1].set_xlabel('Zeit [s]')
        axs[1].set_ylabel('Fehler [m/s]')

        fig.savefig(IMAGE_DIR / f'{simulation}.png')

        print(f"Created new figure: {simulation}")

        plt.close(fig)  # Release memory

    print("Done!")


if __name__ == '__main__':
    main()
