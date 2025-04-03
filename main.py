from visualisation.plots import (
    plot_distance_vs_time_weekly,
    plot_pace_vs_date,
    plot_pace_vs_distance,
    plot_pace_vs_elevation,
    plot_pace_vs_perceived_effort,
)
from input_handler.input_handler import (
    get_dates,
    get_user_id,
    is_valid_date,
    plot_activity_input,
    plot_all_activity_data,
    exit,
)


def activity_plotter():
    """main script for running the activity plotter - it retrieves the
    user_id and dates between which to plot the data, validates the inputs are
    in the correct format, then plots the appropriate graph based on the user
    input.

    If there is no data available to plot, a message is printed stating this."""

    print("Hi, welcome to activity plotter!")

    # retrieve valid user_id
    user_id = get_user_id()
    while not user_id.isnumeric():
        print()
        print("Invalid User ID. User ID it must be a number.")
        print()
        user_id = get_user_id()

    # does the user want to plot all data or specify dates?
    plot_all_data = plot_all_activity_data()
    while plot_all_data == "Invalid input":
        print()
        print("Invalid input.")
        print()
        plot_all_data = plot_all_activity_data()

    # retrieve valid dates between which to plot data
    if plot_all_data:
        start_date = "1981/01/01"
        end_date = "2081/01/01"
    else:
        start_date, end_date = get_dates()
        while not is_valid_date(start_date) and not is_valid_date(end_date):
            print()
            print("Invalid input. Date must be in the format YYYY/MM/DD.")
            print()
            start_date, end_date = get_dates()

    # loop continually runs until "x" (exit) selected
    while True:
        # retrieve valid option for graph to plot
        activity_input = plot_activity_input()
        while activity_input not in ["a", "b", "c", "d", "e", "x"]:
            print()
            print("Invalid input.")
            print()
            activity_input = plot_activity_input()
        # graph plotted based on option selected. Or exits application ("x").
        try:
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
        except KeyError as e:
            print()
            print(
                f"No data available for user_id {user_id} between the dates specified."
            )
            print()


if __name__ == "__main__":
    activity_plotter()
