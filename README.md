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

## How it works
Before explaining the logic flow of operations executing on backend, here's a brief walkthrough, of the thought process leading to the backend architecture of this website.
1. As KKMNOW will only expand in the number of dashboards being added in the future, it would be redundant to have multiple endpoints for each dashboard.
2. KKMNOW may also have multiple different charts being added, as time goes by, these charts may vary on type, constraints, and so much more.

To reduce the code complexity of this project as it moves forward, the design rule of thumb of the backend architecture, is to maintain the number of endpoints on backend as minimal as possible, as well as ensuring that each chart builder could be versatile enough, to generate the required outcome.

### META Jsons version 1.0 ###
A META Json contains all information required to build a dashboard. These files can be found within the `management/commands/META_JSON` folder, within the app. Each of these files are responsible for either a dashboard, or a dedicated chart. Within these META Jsons, are information regarding the required and optional parameters for the API, and the list of charts needed.

Nested within the chart key, are multiple keys which represents the chart's name. Within this object, there are all information required for the chart, such as parameters, chart types, api types, and variables. The variables and `chart_source` keys, are data which would be fed to the chart builders, to build the desired outcome.

### Chart Builders version 1.0 ###
To ensure the versatility of the chart builders, the design principle kept in mind, was to have every chart, of the same chart type, be built using only 1 method. Within the `utils` folder in the project, the `chart_builder` file contains several methods, to build each specific chart type, such as heatmap, bar charts, choropleths, etc. Therefore, for as long as the supplied variables are sufficient, the chart builder can dynamically format the charts' api, following the conditions set by the variables, requiring less 'hard-coded' values, and thus, increasing its versatility.

### API endpoint version 1.0 ###
Despite having several dashboards on KKMNOW, there is only 1 endpoint, serving all dashboards. Every GET request to this endpoint, `kkmnow/`, will have to be associated with a query parameter, `'dashboard'`. This parameter indicates which dashboard API should be returned. There can be multiple parameters as well, and for as long as they're defined in the META Json and individual charts parameter, the `handle_request` method, would be able to operate them accordingly. 