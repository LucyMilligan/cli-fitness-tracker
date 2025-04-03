# cli-fitness-tracker
A simple API and command line interface application to visualise activity data (currently only set up for road/trail running). Users can enter, retrieve, modify and delete user and activity data via an API, with data stored in a postgres database. Users can also create simple plots of the data via a command line interface application to give them some insights into how their training is going.

The aim of this mini project was to practice interacting with a database and creating graphical visualisations in python (using SQLAlchemy, Pandas, Matplotlib and Numpy).

## Prerequisites

Postgres - this can be downloaded from https://www.postgresql.org/download/

## Setup

Clone the repo:

```git clone https://github.com/LucyMilligan/cli-fitness-tracker.git```

Unless explicitly stated, run the following commands in the root of the directory to setup the project. 

Create a virtual environment and install the requirements:

```pip install -r requirements.txt```

Create a .env file in the root of the directory, with the following content, updating the username and password with your postgress username and password:

```DB_URL="postgresql://<username>:<password>@localhost:5432/cli_fitness_tracker"```

Create the database:

```psql -f database/create.sql```

Run the API:

```uvicorn routes:app --reload --port <port: int>```

Seed the database: 

```python seed_db.py```

Note: Prior to seeding the database, the above two steps must be executed. These create the database and tables needed to add data to the database.

## Data entry, retrieval and modification

User and activity data can be entered, retrieved, modified and deleted via the API. Type the following command into the terminal and use the browser to interact with the API and perform get, post, patch and delete requests (localhost:<port: int>/docs).

```uvicorn routes:app --reload --port <port: int>```

## Data visualisation application

To graphically visualise data (e.g. pace vs date), run the main.py file and follow the CLI prompts.

```python main.py```

## Run tests

To run the unit tests:

```pytest -vvvrP```

## Further Improvements

Improvements to the application could be:
- add additional graphs
- give users options to add trendlines to graphs
- accept and process other activities such as cycling
