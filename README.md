# basic-data-visualisation
Practice using tools to visualise data in Python

## Setup

Create a virtual environment and install the requirements

```pip install requirements.txt```

## To run the application

### If database does not exist:

Create a .env file in the root of the directory, with the following content, updating the username and password with your postgress username and password:

```DB_URL="postgresql://<username>:<password>@localhost:5432/fitness_tracker_test_db"```

Create the database by running the following in the terminal:

```psql -f create.sql```

### To run the application:

```uvicorn main:app --reload --port <port: int>```

To test the requests, use the browser and localhost:<port: int>/docs

### To seed the database:

Prior to seeding the database, the above two steps (create database and run application) must be executed. These create the database and tables needed to add data to the database.

```python seed_db.py```

### To plot data

