from sqlalchemy import create_engine, select
import os
from dotenv import load_dotenv
from sqlmodel import Session
from database.database import engine
from database.models import Activity
import pandas as pd

load_dotenv()

postgres_url = os.getenv("DB_URL")

engine = create_engine(postgres_url)


def calculate_time_secs(moving_time: str):
    """calculates the moving time in seconds, given an input moving_time in the format
    "HH:MM:SS. Returns the time in secs as an integer."
    """
    hours, minutes, seconds = map(int, moving_time.split(":"))
    time_secs = seconds + (minutes * 60) + (hours * 60 * 60)
    return time_secs


def calculate_pace_mins_per_km(distance: float, moving_time: str):
    """Calculates the pace of an activity in minutes per km, returning the pace as
    a string in the format "MM:SS"
    """
    time_secs = calculate_time_secs(moving_time)
    pace_secs_per_km = time_secs / distance
    pace_mins = int(pace_secs_per_km // 60)
    pace_secs = int(pace_secs_per_km % 60)
    return f"{pace_mins}:{str(pace_secs).rjust(2, "0")}"


def convert_pace_to_float(pace_string: str):
    """takes a pace string in the format "MM:SS" (min/km) and converts it into a float.
    e.g. "6:53" would return 6.88 min/km. This is for ease of plottin the data."""
    minutes, seconds = map(int, pace_string.split(":"))
    return round((minutes + (seconds / 60)), 2)


def format_query_output(data, col_names):
    """formats query output results into a dictionary.
    
    :param data: list of tuples containing the data, with each tuple representing a row
    :param col_names: list of columns names relating to the data
    :returns: a list of dictionaries containing the data in the format
    [{col_1: data_1, col_2: data_2, col_3: data_3}]
    """
    formatted_data = []
    for row in data:
        formatted_data.append(dict(zip(col_names, row)))
    return formatted_data


def select_activity_data(user_id: int, start_date: str = "1981/01/01", end_date: str = "2081/01/01"):
    """queries the database and returns a list of dictionaries containing the query results.
    
    :param user_id: user id integer
    :param start_date: earliest data for which activity data should be obtained.
    This should be in a string of format "YYYY/MM/DD".
    :param end_date: latest data for which activity data should be obtained.
    This should be in a string of format "YYYY/MM/DD".
    :returns: a list of dictionaries containing the activity data, with each dictionary representing 
    a row of data, keys representing the column name and values representing the data.
    """
    with Session(engine) as session:
        #explicitly unpacking all columns in the Activiy table (to give a list of tuples
        #instead of ORM objects)
        stmt = select(*Activity.__table__.c).where(
                    Activity.date > start_date, Activity.date < end_date)
        activities = session.exec(stmt)
        activities_data = activities.all()
        activities_col_names = activities.keys()

    formatted_activities = format_query_output(activities_data, activities_col_names)
    return formatted_activities


def create_dataframe(data: list):
    """creates a pandas dataframe from given activity data. It converts the date strings
    into datetime format, adds a pace column (string in format "MM:SS", min/km) and adds a 
    pace_numeric column (float, min/km).
    
    :param data: a list of dictionaries containing data, with each dictionary representing 
    a row of data, keys representing the column name and values representing the data.
    :returns: a pandas dataframe representing the data, with the addition of pace and 
    pace_numeric columns. If a date is not parsed in the format "YYYY/MM/DD", NaT (Not a Time)
    is set as the date value.
    """
    df = pd.DataFrame(data)
    df["date"] = pd.to_datetime(df["date"], format="%Y/%m/%d", errors="coerce")
    df["pace"] = df.apply(lambda x: calculate_pace_mins_per_km(x["distance_km"], x["moving_time"]), axis=1)
    df["pace_numeric"] = df["pace"].apply(convert_pace_to_float)
    type(df)
    return df