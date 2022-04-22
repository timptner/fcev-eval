import matplotlib.pyplot as plt

from .helpers import select_item_interactively, get_signal_names, get_index_from_value, ask_user_for_number


def plot_signal(simulation, show_plot=True) -> None:
    """Select a signal by number and plot it over time"""
    signals = get_signal_names(simulation, with_units=True)
    signal_list = [(key, value[0]) for key, value in signals.items()]
    signal = select_item_interactively(signal_list, question="Which signal do you want to plot?")

    max_limit = int(simulation['time'][:].max())
    print("Please provide the lower limit you want the plot.")
    lower_limit = ask_user_for_number(max_limit)
    print("Please provide the range you want to plot.")
    upper_limit = lower_limit + ask_user_for_number(max_limit - lower_limit)
    lower_limit_index = get_index_from_value(simulation['time'][:], lower_limit)
    upper_limit_index = get_index_from_value(simulation['time'][:], upper_limit)

    fig, ax = plt.subplots()
    ax.plot(simulation['time'][lower_limit_index:upper_limit_index],
            simulation['data'][signal][lower_limit_index:upper_limit_index])
    ax.set_xlabel("Zeit [s]")
    ax.set_ylabel(f"{signals[signal][0]} [{signals[signal][1]}]")
    ax.set_title(simulation.attrs['Name'])
    ax.grid()
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

