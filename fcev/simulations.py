import h5py
import typer

from h5py._hl.group import Group as H5Group

from .helpers import select_item_interactively

app = typer.Typer()


@app.command()
def delete(ctx: typer.Context) -> None:
    """Delete simulation from hdf5 file"""
    file: h5py.File = ctx.obj

    simulations = [(value, value.attrs['Name']) for value in file.values()]
    simulation: H5Group = select_item_interactively(simulations, prompt="Available simulations")

    del file[simulation.name]
    typer.secho("Simulation removed successfully.", fg=typer.colors.GREEN)
    file.close()
