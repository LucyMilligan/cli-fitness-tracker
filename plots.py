import matplotlib.pyplot as plt
import numpy as np
from sqlalchemy import create_engine, select
import os
from dotenv import load_dotenv
from sqlmodel import Session
from main import engine, SessionDep
from models import Activity

load_dotenv()

postgres_url = os.getenv("DB_URL")

engine = create_engine(postgres_url)


#simple plot with no meaning
plt.plot([1, 2, 3, 4, 5], [1, 4, 9, 16, 25], "ro")
plt.axis((0, 6, 0, 30)) #xmin, xmax, ymin, ymax
plt.ylabel("some numbers")
plt.xlabel("some more numbers")
# plt.show()

def calculate_time_secs(moving_time: str):
    """calculates the moving time in seconds, given an input moving_time in the format
    "HH:MM:SS. Returns the time in secs as an integer."
    """
    time_secs = int(moving_time[6:]) + (int(moving_time[3:5]) * 60) + (int(moving_time[0:2]) * 60 * 60)
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


def select_activity_data(user_id: int, start_date: str = "1981/01/01", end_date: str = "2081/01/01"):
    with Session(engine) as session:
        stmt = select(
            Activity.id, Activity.distance_km, Activity.moving_time, Activity.date).where(
                Activity.user_id == user_id).where(
                    Activity.date > start_date, Activity.date < end_date)
        activities = session.exec(stmt).all()
    
    print(activities)
    print(stmt)
    

select_activity_data(1, "2025/03/01", "2025/03/20")