# MoviesAndShowsDatabase

A simple Python / MySQL application for movies and tv-shows. This is a project from Database Systems (DV1663) at BTH.

## How to use
### Install dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
```

### Download and import data
This step assumes MySQL is already running on 127.0.0.1 and username=root and password=mysql, change in import.py if values differ from your installation.

Run the following to 1. download the datasets from imdb, 2. only take a bit of it, 3. import it into MySQL.
```bash
python3 import.py
```

