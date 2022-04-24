#! /usr/bin/env python3
import os

import h5py
import typer
import yaml

from pathlib import Path

from . import plotter, durations, simulations

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / 'data'

app = typer.Typer()
app.add_typer(plotter.app, name='plot', help="Plot available data")
app.add_typer(durations.app, name='durations')
app.add_typer(simulations.app, name='simulations')


@app.callback()
def main(ctx: typer.Context):
    config_file = BASE_DIR / 'config.yaml'
    if not config_file.exists():
        typer.secho("Config file not found.", fg=typer.colors.RED)
        raise typer.Abort()

    config = yaml.load(config_file.read_text(), yaml.Loader)
    config['storage_file'] = Path(config['storage_file']).resolve()

    ctx.obj = config
    file_path = config['storage_file']
    try:
        ctx.obj['file'] = h5py.File(file_path, 'a')
    except BlockingIOError:
        msg = typer.style("export HDF5_USE_FILE_LOCKING=FALSE", bg=typer.colors.CYAN)
        typer.echo(f"Run {msg} inside your console.")
        raise typer.Abort()


if __name__ == '__main__':
    app()
