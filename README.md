# OCT Storage API

## Requrements
- python3.7+
- postgres + postgis extension


## Install instructions

1. Create and activate virtual environment for python 3.7 or more (see pyenv)
2. Install python deps `pip install -r requirements_test.txt`
3. create database and activate extension
4. create `instance/local.py` file and set settings based on `oct_storage/config.py`
5. run migrations `make upgrade`
6. run project `python run.py`

## Docker-way
1. Create `instance/local.py` file and set settings based on `oct_storage/config_docker.py`
2. Run docker-compose `docker-compose up --build`
3. In separate Terminal tab go to container `docker exec -it oct-storage_app_1 bash`
4. Run migrations in container: `make upgrade`

## Docs

You can find OpenApi in `docs/api.yaml` and UI https://storage.dev.opencovidtrace.org/docs/

## Test version
You can find latest deployed version for testing https://storage.dev.opencovidtrace.org/
