#! /usr/bin/env python3

"""
Plot durations and save image file to disk.
"""

import matplotlib.pyplot as plt
import pandas as pd

from fcev.__main__ import BASE_DIR, DATA_DIR
from fcev.helpers import mm2inch

IMAGE_DIR = BASE_DIR / 'figures' / 'duration'

EXPLOSION = {
    'strategy': {
        'WLTP_BAT_SOC50': [0, 0, 0.1, 0.5, 0],
        'WLTP_SC_SOC50': [0, 0, 0],
        'Artemis130_BAT_SOC50': [0, 0, 0, 0, 0],
        'Artemis130_SC_SOC50': [0, 0, 0],
    },
    'charging': {
        'WLTP_BAT_SOC50': [0, 0, 0.2],
        'WLTP_SC_SOC50': [0, 0, 0.2],
        'Artemis130_BAT_SOC50': [0, 0, 0.2],
        'Artemis130_SC_SOC50': [0, 0, 0.2],
    },
}


def main() -> None:
    """Main entry-point for script"""
    if not IMAGE_DIR.exists():
        IMAGE_DIR.mkdir(parents=True)

    for item in ['strategy', 'charging']:
        df = pd.read_csv(DATA_DIR / 'processed' / f'durations_{item}.csv', index_col='Simulation')

        for index, data in df.iterrows():
            data = data[data > 0]

            fig, ax = plt.subplots(figsize=(mm2inch(150), mm2inch(70)), dpi=300,
                                   layout='constrained', subplot_kw={'aspect': 'equal'})
            wedges, texts, autotexts = ax.pie(data, autopct='%1.1f%%', pctdistance=0.75, explode=EXPLOSION[item][index],
                                              wedgeprops={'width': 0.5, 'linewidth': 0.7, 'edgecolor': 'white'})
            ax.legend(data.keys(), loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))

            filename = f'{index}_{item}.png'
            fig.savefig(IMAGE_DIR / filename)
            print(f"Figure saved: {filename}")

    print("Done!")


if __name__ == '__main__':
    main()
