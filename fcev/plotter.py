import matplotlib.pyplot as plt

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
