import matplotlib.pyplot as plt
import numpy as np
from sqlalchemy import create_engine, select
import os
from dotenv import load_dotenv
from sqlmodel import Session
from main import engine, SessionDep
from models import Activity
from datetime import datetime, timedelta
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


def plot_pace_vs_date(user_id: int, start_date: str = "1981/01/01", end_date: str = "2081/01/01"):
    """creates a scatter plot of pace vs date for activity data"""
    activities = select_activity_data(user_id, start_date, end_date)
    df = create_dataframe(activities)

    plt.figure(figsize=(12,6))
    plt.plot(df["date"], df["pace_numeric"], marker="o", color="purple", ls="")
    plt.xlabel("Date")
    plt.ylabel("Pace (min/km)")
    plt.title("Pace vs Date")
    plt.gca().invert_yaxis() #slower paces at the bottom
    plt.grid(True)
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()


def plot_pace_vs_elevation(user_id: int, start_date: str = "1981/01/01", end_date: str = "2081/01/01"):
    """creates a scatter plot of pace vs elevation for activity data"""
    activities = select_activity_data(user_id, start_date, end_date)
    df = create_dataframe(activities)

    #plot the figure
    plt.figure(figsize=(12,6))
    plt.plot(df["elevation_m"], df["pace_numeric"], marker="o", color="green", ls="")
    plt.xlabel("Elevation (m)")
    plt.ylabel("Pace (min/km)")
    plt.title("Pace vs Elevation")
    plt.gca().invert_yaxis() #slower paces at the bottom
    plt.grid(True)
    plt.tight_layout()

    #add a trendline (assuming linear trend)
    z = np.polyfit(df["elevation_m"], df["pace_numeric"], 1)
    p = np.poly1d(z)
    plt.plot(df["elevation_m"], p(df["elevation_m"]), color="green", ls="-")

    plt.show()


def plot_pace_vs_distance(user_id: int, start_date: str = "1981/01/01", end_date: str = "2081/01/01"):
    """creates a scatter plot of pace vs distance for activity data"""
    activities = select_activity_data(user_id, start_date, end_date)
    df = create_dataframe(activities)

    #plot the figure
    plt.figure(figsize=(12,6))
    plt.plot(df["distance_km"], df["pace_numeric"], marker="o", color="c", ls="")
    plt.xlabel("Distance (km)")
    plt.ylabel("Pace (min/km)")
    plt.title("Pace vs Distance")
    plt.gca().invert_yaxis() #slower paces at the bottom
    plt.grid(True)
    plt.tight_layout()

    #add a trendline (assuming linear trend)
    z = np.polyfit(df["distance_km"], df["pace_numeric"], 1)
    p = np.poly1d(z)
    plt.plot(df["distance_km"], p(df["distance_km"]), color="c", ls="-")

    plt.show()


def plot_pace_vs_perceived_effort(user_id: int, start_date: str = "1981/01/01", end_date: str = "2081/01/01"):
    """creates a scatter plot of pace vs perceived effort for activity data"""
    activities = select_activity_data(user_id, start_date, end_date)
    df = create_dataframe(activities)

    #plot the figure
    plt.figure(figsize=(12,6))
    plt.plot(df["perceived_effort"], df["pace_numeric"], marker="o", color="orangered", ls="")
    plt.xlabel("Perceived Effort (1 (very easy) to 10 (very hard))")
    plt.ylabel("Pace (min/km)")
    plt.title("Pace vs Perceived Effort")
    plt.gca().invert_yaxis() #slower paces at the bottom
    plt.grid(True)
    plt.tight_layout()

    #add a trendline (assuming linear trend)
    # z = np.polyfit(df["perceived_effort"], df["pace_numeric"], 1)
    # p = np.poly1d(z)
    # plt.plot(df["perceived_effort"], p(df["perceived_effort"]), color="orangered", ls="-")

    plt.show()


def plot_distance_vs_time_weekly(user_id: int, start_date: str = "1981/01/01", end_date: str = "2081/01/01"):
    """creates a bar chart of total weekly distance effort for activity data"""
    activities = select_activity_data(user_id, start_date, end_date)
    df = create_dataframe(activities)
    filtered_df = df.filter(["distance_km", "date"])
    weekly_data = filtered_df.groupby(pd.Grouper(key="date", freq="W")).sum().fillna(0)

    plt.figure(figsize=(12,6))
    plt.bar(weekly_data.index, weekly_data["distance_km"], width=5, color="gold")
    plt.xlabel("Date")
    plt.ylabel("Total Distance (km)")
    plt.title("Weekly running distance")
    plt.tight_layout()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.grid(axis="y")

    plt.show()

### To test different plots ###
# plot_pace_vs_date(1)
# plot_pace_vs_elevation(1)
# plot_pace_vs_distance(1)
# plot_pace_vs_perceived_effort(1)
# plot_distance_vs_time_weekly(1)