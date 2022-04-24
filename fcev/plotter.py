import h5py
import matplotlib.pyplot as plt
import typer

from h5py._hl.group import Group as H5Group
from pathlib import Path

from .helpers import select_item_interactively, get_unique_image_name, get_index_from_value, ask_user_for_number, mm2inch

BASE_DIR = Path(__file__).resolve().parent.parent

IMAGE_DIR = BASE_DIR / 'images'

FIG_SIZE = (mm2inch(160), mm2inch(100))
DPI = 300

app = typer.Typer()


@app.command('signal')
def signal_over_time(ctx: typer.Context) -> None:
    """Select a signal by number and plot it over time"""
    file: h5py.File = ctx.obj['file']

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

    fig, ax = plt.subplots(figsize=FIG_SIZE, dpi=DPI, constrained_layout=True)
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
def duration_of_sets(ctx: typer.Context) -> None:
    """Plot a calculated duration as pie chart"""
    config = ctx.obj
    file: h5py.File = config['file']

    simulations = [(value, value.attrs['Name']) for value in file.values()]
    simulation: H5Group = select_item_interactively(simulations, prompt="Available simulations")

    if 'calculated' not in simulation.keys():
        typer.secho("Simulation does not have any calculations to plot.", fg=typer.colors.RED)
        raise typer.Abort()

    calculations = simulation['calculated']
    durations = [(value, value.attrs['Signal']) for key, value in calculations.items() if key.startswith('duration_')]
    if not durations:
        typer.secho("Simulation does not have any durations calculated.", fg=typer.colors.RED)
        raise typer.Abort()

    duration = select_item_interactively(durations, prompt="Available durations")
    sets = [(value.attrs['Name'], value[0]) for key, value in duration.items()]
    labels, data = zip(*sets)

    fig, ax = plt.subplots(figsize=FIG_SIZE, dpi=DPI, constrained_layout=True)
    ax.pie(data, autopct='%1.1f%%', wedgeprops={"linewidth": 1, "edgecolor": "white"})
    ax.set_title(f"{simulation.attrs['Name']}: {duration.attrs['Signal']}")
    ax.legend(labels, loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))

    file_path = get_unique_image_name(IMAGE_DIR, 'duration')
    fig.savefig(file_path)
    msg = typer.style(file_path.stem, fg=typer.colors.CYAN)
    typer.echo(f"Plot saved as {msg}!")

    if typer.confirm("Do you want to display the plot?"):
        plt.show()

