from visualisation.plots import plot_distance_vs_time_weekly, plot_pace_vs_date, plot_pace_vs_distance, plot_pace_vs_elevation, plot_pace_vs_perceived_effort
from visualisation.utils import get_dates, get_user_id, plot_activity_input, plot_all_activity_data, exit


def activity_plotter():
    """main script for running the activity plotter - it retrieves the
    user_id and dates between which to plot the data, then plots the
    appropriate graph based on the user input."""
    print("Hi, welcome to activity plotter!")
    user_id = get_user_id()
    plot_all_data = plot_all_activity_data()
    if plot_all_data:
        start_date = "1981/01/01"
        end_date = "2081/01/01"
    else:
        start_date, end_date = get_dates()
    
    while True:
        activity_input = plot_activity_input()
        if activity_input == "x":
            exit()
        elif activity_input == "a":
            plot_pace_vs_date(user_id, start_date, end_date)
        elif activity_input == "b":
            plot_pace_vs_distance(user_id, start_date, end_date)
        elif activity_input == "c":
            plot_pace_vs_elevation(user_id, start_date, end_date)
        elif activity_input == "d":
            plot_pace_vs_perceived_effort(user_id, start_date, end_date)
        elif activity_input == "e":
            plot_distance_vs_time_weekly(user_id, start_date, end_date)


if __name__ == "__main__":
    activity_plotter()