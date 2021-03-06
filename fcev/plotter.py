import h5py
import matplotlib.pyplot as plt
import numpy as np
import typer

from h5py._hl.group import Group as H5Group
from pathlib import Path

from .helpers import select_item_interactively, get_unique_image_name, get_index_from_value, ask_user_for_number, mm2inch

BASE_DIR = Path(__file__).resolve().parent.parent

IMAGE_DIR = BASE_DIR / 'images'

app = typer.Typer()


@app.command('signal')
def signal_over_time(ctx: typer.Context) -> None:
    """Select a signal by number and plot it over time"""
    config = ctx.obj
    file: h5py.File = config['file']

    simulations = [(value, value.attrs['Name']) for value in file.values()]
    simulation: H5Group = select_item_interactively(simulations, prompt="Available simulations")

    time = simulation['time'][:]

    signals = [(value, value.attrs['Name']) for value in simulation['data'].values()]
    signal = select_item_interactively(signals, prompt="Available signals")

    max_upper_limit = int(time.max())
    lower_limit = ask_user_for_number(max_upper_limit, prompt="Starting point [s]")
    upper_limit = lower_limit + ask_user_for_number(max_upper_limit - lower_limit, prompt="Duration [s]")

    lower_limit_index = get_index_from_value(time, lower_limit)
    upper_limit_index = get_index_from_value(time, upper_limit)

    config_plots = config['plots']
    config_signals = config_plots['singals']
    figure_size = config_signals['figsize']

    fig, ax = plt.subplots(figsize=(mm2inch(figure_size['width']), mm2inch(figure_size['height'])),
                           dpi=config_plots['dpi'], constrained_layout=True)
    ax.plot(time[lower_limit_index:upper_limit_index], signal[lower_limit_index:upper_limit_index])
    ax.set_xlabel("Zeit [s]")
    ax.set_ylabel(f"{signal.attrs['Name']} [{signal.attrs['Unit']}]")
    ax.set_title(simulation.attrs['Name'])
    ax.grid()

    file_path = get_unique_image_name(IMAGE_DIR, 'signal')
    fig.savefig(file_path)
    msg = typer.style(file_path.stem, fg=typer.colors.CYAN)
    typer.echo(f"Plot saved as {msg}!")

    if typer.confirm("Do you want to display the plot?"):
        plt.show()


@app.command('duration')
def duration_of_groups(ctx: typer.Context) -> None:
    """Plot a calculated duration as pie chart"""
    config = ctx.obj
    file: h5py.File = config['file']

    simulations = [(value, value.attrs['Name']) for value in file.values()]
    simulation: H5Group = select_item_interactively(simulations, prompt="Available simulations")

    if 'calculated' not in simulation.keys():
        typer.secho("Simulation does not have any calculations to plot.", fg=typer.colors.RED)
        raise typer.Abort()

    calculations = simulation['calculated']
    durations = [(value, value.attrs['Signal']) for key, value in calculations.items() if key.startswith('duration')]
    if not durations:
        typer.secho("Simulation does not have any durations calculated.", fg=typer.colors.RED)
        raise typer.Abort()

    duration = select_item_interactively(durations, prompt="Available durations")
    groups = [(value.attrs['Name'], value[0]) for key, value in duration.items()]

    config_plots = config['plots']
    config_duration = config_plots['durations']
    config_signal = config_duration[simulation.attrs['Name']][duration.attrs['Signal']]

    labels, data = zip(*groups)
    order = config_signal['order']
    if len(labels) != len(order):
        raise ValueError("Group count does not match order count. Fix DISPLAY_ORDER")
    if set(labels) != set(order):
        raise ValueError("Group labels do not match order labels. Fix DISPLAY_ORDER")
    labels, data = zip(*[groups[labels.index(key)] for key in order])

    figure_size = config_duration['figsize']
    fig, ax = plt.subplots(figsize=(mm2inch(figure_size['width']), mm2inch(figure_size['height'])),
                           dpi=config_plots['dpi'], layout='constrained', subplot_kw={'aspect': 'equal'})
    wedges, texts, autotexts = ax.pie(data, autopct='%1.1f%%', pctdistance=0.75, explode=config_signal['explode'],
                                      wedgeprops={'width': 0.5, 'linewidth': 0.7, 'edgecolor': 'white'})
    ax.legend(labels, loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))

    file_path = get_unique_image_name(IMAGE_DIR, 'duration')
    fig.savefig(file_path)

    msg = typer.style(file_path.stem, fg=typer.colors.CYAN)
    typer.echo(f"Plot saved as {msg}!")

    if typer.confirm("Do you want to display the plot?"):
        plt.show()

