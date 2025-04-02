import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from visualisation.plots_utils import create_dataframe, select_activity_data


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
