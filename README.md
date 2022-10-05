# kkmnow-back

The backend API for KKMNOW that serves data available via [`MoH-Malaysia/kkmnow-data`](https://github.com/MoH-Malaysia/kkmnow-data) to the frontend at [`MoH-Malaysia/kkmnow-front`](https://github.com/MoH-Malaysia/kkmnow-front). 
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
As of now, KKMNOW uses GitHub Actions to trigger a rebuild (when there is new code) or update of data (when there is new data). Alternatively, with your preferred deployment setup, there are 2 ways to update the data.
- Using POST method
  - A post request can be sent to the endpoint `https://<your url here>/kkmnow/` , which would by default trigger an update, and populate the DB with the new data.
- Using command line
  - Alternatively, if your desired cron / task scheduler runs locally, you could use the command `python manage.py loader UPDATE` , to trigger an update and populate the DB with the new data.

## Private tokens required:
- GitHub token -  Required for interacting with the GitHub API to pull data from the `kkmnow-data` repo.
- Telegram ChatID and token - The KKMNOW backend loader updates status messages to a private Telegram channel for the development team to monitor data pipelines daily. Feel free to comment out any calls to the `trigger` module for the loader to work without Telegram updates.

## How it works
Before explaining the logic of KKMNOW's backend operations, here is a brief description of the thinking behind our architecture choices:
1. KKMNOW will only keep expanding as more dashboards are added, so we wanted to ensure that the number of endpoints did not balloon along with it.
2. KKMNOW will likely include more chart types over time, which may vary in what they require in terms of API structure and business logic.

Therefore, to minimise complexity, it was vital that we used an architecture that could keep the number of endpoints minimal, while simultaneously ensuring that chart data could be served in as versatile a manner as possible. Here are the key ingredients we used to do this:

### META Jsons version 1.0 ###
A META Json contains all information required to build a dashboard. These files can be found within the `management/commands/META_JSON` folder, within the app. Each one is responsible for either a dashboard, or a dedicated chart.
- Each META Json contains information regarding the required and optional parameters for the API, and the list of charts needed.
- Each chart key contains multiple sub-keys representing chart names.
- Each sub-key contains all information required to fully specify a chart, such as parameters, chart types, API types, and variables. 
- The variables and `chart_source` keys contain data which is fed to the chart builders, which serves the final data.

### Chart Builders version 1.0 ###
Critical design principle: All charts of the same type should be built using only 1 method. For instance, all time series charts on the site should (as far as possible) be handled by the same code unit. 
- Within the `utils` folder in the project, the `chart_builder` file contains several methods for various charts, such as heatmaps, bar charts, choropleths, etc.
- As long as sufficient information is supplied (by the META Json), the chart builder can dynamically format a chart's api, thus requiring no 'hard-coding'. This increases versatility.

### API endpoint version 1.0 ###
Despite KKMNOW having 8 dashboards as of 5th October, there is only 1 endpoint which serves all dashboards.
- Every GET request to this endpoint, `kkmnow/`, will have to be associated with a query parameter, `'dashboard'`. 
- This `dashboard` parameter indicates which dashboard API should be returned. 
- There can be multiple parameters as long as they are defined in the META Json and individual charts' parameter - this enables the `handle_request` method to execute them accordingly.
