import matplotlib.pyplot as plt

from matplotlib.patches import Rectangle
from typing import Union, Tuple


def mm2inch(value: Union[int, Tuple[int]]) -> Union[int]:
    def calc(val):
        return round(val / 25.4, 2)
    
    if type(value) == tuple:
        return tuple([calc(i) for i in value])
    elif type(value) == int:
        return calc(value)
    else:
        raise ValueError("Only integers or tuple of integers are allowed.")


FIGSIZE = mm2inch((100,70))
DPI = 300.0


# %% RegBrakeFuCeOff

fig, ax = plt.subplots(figsize=FIGSIZE, dpi=DPI, constrained_layout=True)

ax.set_xlabel("Drehzahl [1/min]")
ax.set_ylabel("Motorleistung (elektrisch) [W]")

ax.axis([0, 4000, -100, 200])

patches = [
    Rectangle((0, -100), 4000, 90, color=(0.1, 0.2, 0.7, 0.3), hatch='\\', label="Beitritt"),
    Rectangle((0, -100), 4000, 100, color=(0.1, 0.7, 0.2, 0.3), hatch='/', label="Halten"),
]

for patch in patches[::-1]:
    ax.add_patch(patch)

ax.set_title("Rekuperation")
ax.legend(handles=patches)


# %% ElecDrive

fig, ax = plt.subplots(figsize=FIGSIZE, dpi=DPI, constrained_layout=True)

ax.set_xlabel("Geschwindigkeit [m/s]")
ax.set_ylabel("Ladezustand [-]")

ax.axis([0, 100, 0, 1])

patches = [
    Rectangle((0, 0.2), 25, 0.8, color=(0.1, 0.2, 0.7, 0.3), hatch='/', label="Beitritt"),
    Rectangle((0, 0.15), 30, 0.85, color=(0.1, 0.7, 0.2, 0.3), hatch='\\', label="Halten"),
]

for patch in patches[::-1]:
    ax.add_patch(patch)

ax.set_title("Elektrisches Fahren")
ax.legend(handles=patches)


# %% RegBrakeFuCeOn

fig, ax = plt.subplots(figsize=FIGSIZE, dpi=DPI, constrained_layout=True)

ax.set_xlabel("Leistung der Brennstoffzelle [W]")
ax.set_ylabel("Ladezustand [-]")

ax.axis([0, 100, 0, 1])

patches = [
    Rectangle((0.8, 0), 25, 0.6, color=(0.1, 0.2, 0.7, 0.3), hatch='/', label="Beitritt"),
    Rectangle((0.9, 0), 30, 0.6, color=(0.1, 0.7, 0.2, 0.3), hatch='\\', label="Halten"),
]

for patch in patches[::-1]:
    ax.add_patch(patch)

ax.set_title("Lastpunktverschiebung")
ax.legend(handles=patches)

plt.show()
