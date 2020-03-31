COVID App Tracks API

Requrements
- python3.7+
- postgres + postgis extension


Install instructions

1. Create and activate virtual environment for python 3.7 or more (see pyenv)
2. Install python deps `pip install -r requirements_test.txt`
3. create database and activate extension
4. create `instance/local.py` file and set settings based on `covid_api/config.py`
5. run migrations `make upgrade`
6. run project `python run.py`


Docs

You can find OpenApi in `docs/api.yaml` and UI http://covidapi-tracks.dev.1check.in/docs/