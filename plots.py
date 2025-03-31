import matplotlib.pyplot as plt
import numpy as np
from sqlalchemy import create_engine, select
import os
from dotenv import load_dotenv
from sqlmodel import Session
from main import engine, SessionDep
from models import Activity
from datetime import datetime
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


def calculate_speed_mins_per_km(distance: float, moving_time: str):
    """Calculates the speed of an activity in minutes per km, returning the speed as
    a string in the format "MM:SS"
    """
    time_secs = calculate_time_secs(moving_time)
    speed_secs_per_km = time_secs / distance
    speed_mins = int(speed_secs_per_km // 60)
    speed_secs = int(speed_secs_per_km % 60)
    return f"{speed_mins}:{str(speed_secs).rjust(2, "0")}"


def convert_speed_to_float(speed_string: str):
    """takes a speed string in the format "MM:SS" and converts it into a float.
    e.g. "6:53" would return 6.88"""
    minutes, seconds = map(int, speed_string.split(":"))
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


#TODO: change so that all data is selected - can be cut down in the dataframes
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
        stmt = select(
            Activity.user_id, Activity.id, Activity.distance_km, Activity.moving_time, Activity.date).where(
                Activity.user_id == user_id).where(
                    Activity.date > start_date, Activity.date < end_date)
        activities = session.exec(stmt)
        activities_data = session.exec(stmt).all()
        activities_col_names = activities.keys()

    formatted_activities = format_query_output(activities_data, activities_col_names)
    
    return formatted_activities

#TODO: test this
def plot_pace_vs_date(user_id: int, start_date: str = "1981/01/01", end_date: str = "2081/01/01"):
    activities = select_activity_data(user_id, start_date, end_date)
    df = pd.DataFrame(activities)
    df["date"] = pd.to_datetime(df["date"], format="%Y/%m/%d", errors="coerce")
    df["pace"] = df.apply(lambda x: calculate_speed_mins_per_km(x["distance_km"], x["moving_time"]), axis=1)
    df["speed_numeric"] = df["speed"].apply(convert_speed_to_float)

    plt.figure(figsize=(12,6))
    plt.plot(df["date"], df["speed_numeric"], marker="o", color="purple")
    plt.xlabel("Date")
    plt.ylabel("Pace (min/km)")
    plt.gca().invert_yaxis() #slower speeds at the bottom
    plt.grid(True)
    plt.xticks(rotation=90)
    plt.show()


#plots:
    #pace vs date
    #pace vs distance
    #pace vs elevation


##################### NOTES / TRYING THINGS OUT - TO REMOVE ########################
# ##### creating a dataframe from a dictionary
# activities = select_activity_data(1)
# df = pd.DataFrame(activities)

# ##### filtering a dataframe
# new_df = df.filter(["distance_km", "moving_time", "date"])

# ##### sorting a dataframe
# sorted_new_df = new_df.sort_values(by=["date"], ascending=True)

# ##### creating a speed column to an existing df
# df["speed"] = df.apply(lambda x: calculate_speed_mins_per_km(x["distance_km"], x["moving_time"]), axis=1)

# ##### converting date string into dateformat (YYYY-MM-DD) on existing df
# df["date"] = pd.to_datetime(df["date"], format="%Y/%m/%d", errors="coerce")

# ##### plot date vs speed
# date_speed_df = df.filter(["date", "speed"])
# date_speed_df["speed_numeric"] = date_speed_df["speed"].apply(convert_speed_to_float)
# plt.figure(figsize=(12,6))
# plt.plot(date_speed_df["date"], date_speed_df["speed_numeric"], marker="o", color="purple")
# plt.xlabel("Date")
# plt.ylabel("Pace (min/km)")
# plt.gca().invert_yaxis() #slower speeds at the bottom
# plt.grid(True)
# plt.xticks(rotation=90)
# plt.show()

# ##### to get a date from a string:
# my_date = "2025/03/31"
# my_date_object = datetime.strptime(my_date, "%Y/%m/%d").date()
# print(my_date_object)
# print(type(my_date_object))

# ##### simple plot with no meaning
# plt.plot([1, 2, 3, 4, 5], [1, 4, 9, 16, 25], "ro")
# plt.axis((0, 6, 0, 30)) #xmin, xmax, ymin, ymax
# plt.ylabel("some numbers")
# plt.xlabel("some more numbers")
# plt.show()