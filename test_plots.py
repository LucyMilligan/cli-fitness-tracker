from plots import calculate_speed_mins_per_km, calculate_time_secs

class TestCalculateTimeSecs:
    def test_calculate_time_secs_just_secs(self):
        moving_time = "00:00:40"
        expected = 40
        result = calculate_time_secs(moving_time)
        assert result == expected

    def test_calculate_time_secs_munites_and_secs(self):
        moving_time = "00:02:30"
        expected = 150
        result = calculate_time_secs(moving_time)
        assert result == expected

    def test_calculate_time_secs_hours_munites_and_secs(self):
        moving_time = "01:01:30"
        expected = 3690
        result = calculate_time_secs(moving_time)
        assert result == expected


class TestCalculateSpeed:
    def test_calculate_speed_min_per_km_30_mins(self):
        moving_time = "00:30:00"
        distance = 5.0
        expected = "6:00"
        result = calculate_speed_mins_per_km(distance, moving_time)
        assert result == expected

    def test_calculate_speed_min_per_km_33_mins(self):
        moving_time = "00:33:00"
        distance = 5.0
        expected = "6:36"
        result = calculate_speed_mins_per_km(distance, moving_time)
        assert result == expected

    
    def test_calculate_speed_min_per_km_greater_than_10_mins_per_km(self):
        moving_time = "02:15:30"
        distance = 5.0
        expected = "27:06"
        result = calculate_speed_mins_per_km(distance, moving_time)
        assert result == expected