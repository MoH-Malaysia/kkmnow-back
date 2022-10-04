# kkmnow-back

The backend API for KKMNOW that serves data available on [`MoH-Malaysia/kkmnow-data`](https://github.com/MoH-Malaysia/kkmnow-data) to the frontend at [`MoH-Malaysia/kkmnow-front`](https://github.com/MoH-Malaysia/kkmnow-front). 
- Django app name: `kkmnow`
- Database: `postgresql`

## Setup virtual environment

```bash
<your python exe> -m venv env

# activate and install dependencies
source env/bin/activate
pip install -r requirements.txt
```

## Setup DB

1. Setup a DB server (PostgresSQL DB recommended) and populate your DB instance settings in the `.env` file.
2. Run migrations to setup all tables: `python manage.py migrate`
3. Fetch data from `MoH-Malaysia/kkmnow-data` repo and populate or update the DB: `python manage.py loader UPDATE`
4. To rebuild the DB from scratch: `python manage.py loader REBUILD`

## Run Development Server
`python manage.py runserver`

## API Endpoint

API will be running at `http://127.0.0.1:8000/kkmnow/`

## Fetching new data
As of now, KKMNOW uses github actions to trigger a rebuild or update of data, every time an updated dataset is pushed. Alternatively, on your preferred setup, there are 2 possible ways to update the data.
- Using POST method
  - A post request can be sent to the endpoint `https://<your url here>/kkmnow/` , which would by default trigger an update, and populate the DB with the new data.
- Using command line
  - Alternatively, if your desired cron / task scheduler runs locally, you could use the command `python manage.py loader UPDATE` , to trigger an update and populate the DB with the new data.

## Other notes
- Private tokens required:
  - GitHub token -  Required for interacting with the GitHub API to pull data from the `kkmnow-data` repo.
  - Telegram ChatID and token - The KKMNOW backend loader updates status messages to a private Telegram channel for the development team to monitor data pipelines daily. Feel free to comment out any calls to the `trigger` module for the loader to work without Telegram updates.
- All work in this repo so far prioritises its main deployment as the backend API for KKMNOW and hence may not immediately be useful nor inituitive for running locally. We will however work on improving this with time.
