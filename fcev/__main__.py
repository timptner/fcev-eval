#! /usr/bin/env python3

from pathlib import Path

from .calculate_duration import main as calc_dur, plot_signal
from .helpers import select_func_interactively

PROJECT_DIR = Path(__file__).resolve().parent.parent


def main() -> None:
    """Main entry-point for script"""
    options = [
        ("Calculate duration of a signal", calc_dur),
        ("Plot signal over time", plot_signal)
    ]
    func = select_func_interactively(options)
    func()


if __name__ == '__main__':
    main()
