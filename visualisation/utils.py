import re
import sys


def get_user_id():
    """gets and returns user_id (int)"""
    user_id = input("Please enter your User ID: ")
    if user_id.isnumeric():
        return user_id
    else:
        print()
        print("Invalid User ID. User ID it must be a number.")
        print()
        get_user_id()


def plot_all_activity_data():
    """gets user input for whether to plot all data or plot 
    activities between specific dates. Returns True if
    the user would like all data to be plotted, and False if not."""
    plot_all_data = input("Would you like to plot all activity data? y/n: ")
    if plot_all_data in ["y", "Y", "n", "N"]:
        return True if plot_all_data.lower() == "y" else False
    else:
        print()
        print("Invalid input.")
        print()
        plot_all_activity_data()


def is_valid_date(date_string):
    """checks whether an entered date is in the correct format
    of YYYY/MM/DD, returning True if it is and False if it isn't."""
    # \d{4} checks if there are 4 digits
    # 0[1-9]|1[0-2] checks if the month is between 01 and 12 
    # \d{2}$ checks that there are exactly 2 last digits
    pattern = r'^\d{4}/(0[1-9]|1[0-2])/\d{2}$'
    match_object = re.match(pattern, date_string)
    return True if match_object else False


def get_dates():
    """gets and returns start and end dates as a tuple (start_date, end_date)"""
    start_date = input("Please enter a start date (YYYY/MM/DD): ")
    end_date = input("Please enter an end date (YYYY/MM/DD): ")
    start_date_valid = is_valid_date(start_date)
    end_date_valid = is_valid_date(end_date)
    if start_date_valid and end_date_valid:
        return (start_date, end_date)
    else:
        print()
        print("Invalid input. Date must be in the format YYYY/MM/DD.")
        print()
        get_dates()


def plot_activity_input():
    """obtains and returns user input for which action they would like to take - actions
    include plotting certain graphs or exiting the application. Returned value is a
    single letter string (e.g. "a").
    """
    print("Available plots and actions:")
    print(" [a] Plot Pace vs Date ")
    print(" [b] Plot Pace vs Distance ")
    print(" [c] Plot Pace vs Elevation ")
    print(" [d] Plot Pace vs Perceived Effort ")
    print(" [e] Plot Weekly Distance vs Date ")
    print(" [x] Exit application ")
    print()
    query = (
        "Please enter the letter of the action you would like to take: "
    )
    user_input = input(query)
    if user_input in ["a", "b", "c", "d", "e", "x"]:
        return user_input
    else:
        print()
        print("Invalid input.")
        print()
        plot_activity_input()


def exit():
    """exits the programme"""
    sys.exit("Goodbye! Enjoy your next activity!")
