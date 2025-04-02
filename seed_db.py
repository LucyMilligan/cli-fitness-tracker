from sqlmodel import Session
from database.models import Activity, User
from database.database import engine


def create_users():
    user_1 = User(name="luc", email="luc@gmail.com")
    user_2 = User(name="bob", email="bob@gmail.com")
    user_3 = User(name="sam", email="sam@gmail.com")

    session = Session(engine)

    session.add(user_1)
    session.add(user_2)
    session.add(user_3)

    session.commit()


def create_activities():
    activity_1 = Activity(
        user_id=1,
        date="2025/03/25",
        time="20:16",
        activity="run",
        activity_type="road",
        moving_time="00:49:21",
        distance_km=7.16,
        perceived_effort=5,
        elevation_m=94,
    )
    activity_2 = Activity(
        user_id=1,
        date="2025/03/23",
        time="10:08",
        activity="run",
        activity_type="road",
        moving_time="00:33:01",
        distance_km=5.01,
        perceived_effort=8,
        elevation_m=89,
    )
    activity_3 = Activity(
        user_id=1,
        date="2025/03/18",
        time="14:40",
        activity="run",
        activity_type="trail",
        moving_time="01:16:22",
        distance_km=10.60,
        perceived_effort=4,
        elevation_m=146,
    )
    activity_4 = Activity(
        user_id=1,
        date="2025/03/16",
        time="09:02",
        activity="run",
        activity_type="road",
        moving_time="00:52:38",
        distance_km=6.89,
        perceived_effort=3,
        elevation_m=104,
    )
    activity_5 = Activity(
        user_id=1,
        date="2025/03/12",
        time="17:02",
        activity="run",
        activity_type="road",
        moving_time="00:37:53",
        distance_km=5.14,
        perceived_effort=3,
        elevation_m=46,
    )
    activity_5 = Activity(
        user_id=1,
        date="2025/03/05",
        time="17:45",
        activity="run",
        activity_type="road",
        moving_time="00:33:24",
        distance_km=5.01,
        perceived_effort=6,
        elevation_m=36,
    )
    activity_6 = Activity(
        user_id=1,
        date="2025/02/27",
        time="17:45",
        activity="run",
        activity_type="road",
        moving_time="00:34:01",
        distance_km=5.01,
        perceived_effort=6,
        elevation_m=81,
    )
    activity_7 = Activity(
        user_id=1,
        date="2025/02/22",
        time="17:12",
        activity="run",
        activity_type="road",
        moving_time="00:30:56",
        distance_km=5.02,
        perceived_effort=7,
        elevation_m=43,
    )
    activity_8 = Activity(
        user_id=1,
        date="2025/02/17",
        time="17:34",
        activity="run",
        activity_type="road",
        moving_time="00:32:15",
        distance_km=5.01,
        perceived_effort=6,
        elevation_m=50,
    )
    activity_9 = Activity(
        user_id=1,
        date="2025/02/10",
        time="17:28",
        activity="run",
        activity_type="road",
        moving_time="00:38:57",
        distance_km=5.59,
        perceived_effort=6,
        elevation_m=103,
    )
    activity_10 = Activity(
        user_id=1,
        date="2025/02/03",
        time="17:29",
        activity="run",
        activity_type="road",
        moving_time="00:37:25",
        distance_km=5.20,
        perceived_effort=8,
        elevation_m=116,
    )
    activity_11 = Activity(
        user_id=1,
        date="2025/01/29",
        time="17:35",
        activity="run",
        activity_type="road",
        moving_time="00:32:02",
        distance_km=5.01,
        perceived_effort=5,
        elevation_m=49,
    )

    session = Session(engine)

    session.add(activity_1)
    session.add(activity_2)
    session.add(activity_3)
    session.add(activity_4)
    session.add(activity_5)
    session.add(activity_6)
    session.add(activity_7)
    session.add(activity_8)
    session.add(activity_9)
    session.add(activity_10)
    session.add(activity_11)

    session.commit()


if __name__ == "__main__":
    create_users()
    create_activities()
