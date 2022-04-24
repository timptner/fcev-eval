# FCEV-Eval

This repository is a collection of python scripts which are used to evaluate 
and plot the data from the simulation project "Fuel Cell Electrical Vehicle".

## Project structure

```
./root/
├── data/
│   ├── raw/            Raw binary data
│   ├── cleaned/        Cleaned data
│   └── processed/      Calculated data
├── fcev/               Source code
├── figures/            Graphical plots
└── script/             Scripts to clean data and do calculations
```

## Setup

Create a python virtual environment and activate it.

```bash
python -m venv ./venv
source venv/bin/activate
```

Install all dependencies from `./requirements.txt`.

```bash
python -m pip install -r requirements.txt
```

Install the project as editable package inside virtualenv.

```bash
python -m pip install -e .
```

Execute scripts from the folder `./scripts/`.

```bash
cd scripts
python <script_name>.py
```
