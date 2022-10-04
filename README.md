# kkmnow-back

The backend API repo for KKMNOW
- Django app name: `kkmnow`
- Database: `postgresql`
- API Cache: `redis`

## Setup virtual environment

```
<your python exe> -m venv env
source env/bin/activate
pip install -r requirements.txt
```

## Setup DB

1. Setup a DB server (PostgresSQL DB recommended)
2. Run django migrations: `python manage.py migrate`
3. Fetch data from `MoH-Malaysia/kkmnow-data` repo and populate or update the DB: `python manage.py loader UPDATE`
4. To rebuild the DB from scratch: `python manage.py loader REBUILD`

## Run Development Server
`python manage.py runserver`

## API Endpoint

API will be running at `http://127.0.0.1:8000/kkmnow/`


