import matplotlib.pyplot as plt
import numpy as np

from .helpers import select_item_interactively, get_signal_names


def plot_data(simulation, signal: str) -> None:
    """Create new plot to show data"""
    signals = get_signal_names(simulation, show_units=True)
    fig, ax = plt.subplots()
    ax.plot(simulation['time'][:], simulation['data'][signal][:])
    ax.set_xlabel('Zeit [s]')
    ax.set_ylabel(signals[signal])
    ax.set_title(simulation.attrs['Name'])


def plot_signal(simulation, show_plot=True) -> None:
    """Select a signal by number and plot it over time"""
    signals = get_signal_names(simulation)
    signal_list = [(key, value) for key, value in signals.items()]
    signal = select_item_interactively(signal_list, question="Which signal do you want to plot?")
    plot_data(simulation, signal.split('|')[0])
    if show_plot:
        plt.show()


def plot_duration(simulation, show_plot=True) -> None:
    """Plot a calculated duration as pie chart"""
    if 'calculated' not in simulation.keys():
        raise KeyError("No calculations for this simulation found.")
    group = simulation['calculated']
    durations = [key for key in group.keys() if key.startswith('duration_')]
    if not durations:
        raise ValueError("No durations are calculated for this simulation. Run calculations first!")
    duration_list = [(duration, group[duration].attrs['Signal']) for duration in durations]
    duration = select_item_interactively(duration_list, "Which signal duration do you want to plot?")
    subgroup = group[duration]
    labels, data = zip(*[(value.attrs['Name'], value[0]) for key, value in subgroup.items()])

    fig, ax = plt.subplots()
    ax.pie(data, autopct='%1.1f%%', wedgeprops={"linewidth": 1, "edgecolor": "white"})
    ax.set_title(f"{simulation.attrs['Name']}: {subgroup.attrs['Signal']}")
    # TODO move legend to top or make bigger bounding box
    ax.legend(labels, loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
    if show_plot:
        plt.show()

