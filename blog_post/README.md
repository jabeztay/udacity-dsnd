# PUBG Data Project

## Tools used

Running `pip install -r requirements.txt` should provide all dependencies.

The following packages were used in this project:
- `numpy==1.15.4`
- `pandas==0.23.4`
- `matplotlib==3.0.2`
- `seaborn==0.9.0`
- `Pillow==5.3.0`
- `jupyterlab==0.35.4`
- `chicken-dinner==0.6.0`

You will need a [PUBG API key](https://developer.playbattlegrounds.com/) if
you would like to get new data.

Edit `get_data.py` and `helper_py` as necessary to fetch different data.

## Project Motivation

As an average PUBG player, I'd like to find out if there's anything I could
do to improve my game play (besides having a better accuracy).

- Which locations are hot drop zones?
- Is there a weapon that stands out above the rest?
  - What weapons get picked up the most?
  - What weapons get the most kills?
  - Deal the most damage?

## File Descriptions

- `helper.py`: helper functions to get data
- `get_data.py`: run to get data, edit shard as needed
- `data/matches.csv`: contains basic match information
- `Explore Data.ipynb`: exploration of data - Sanhok
- `maps`: maps from PUBG api
- `dictionaries`: dictionary from PUBG api

## Results

Work in progress...
