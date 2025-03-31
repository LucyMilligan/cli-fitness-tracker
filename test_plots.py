from plots import calculate_speed_mins_per_km, calculate_time_secs, convert_speed_to_float, format_query_output, select_activity_data

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


class TestConvertSpeedToFloat:
    def test_convert_speed_to_float(self):
        speed_string = "6:53"
        result = convert_speed_to_float(speed_string)
        assert result == 6.88


class TestFormatQueryOutput:
    def test_format_query_output_single_row(self):
        data = [("test1", "test2", "test3")]
        col_names = ["col1", "col2", "col3"]
        result = format_query_output(data, col_names)
        assert result == [{"col1": "test1", "col2": "test2", "col3": "test3"}]

    def test_format_query_output_multiple_rows(self):
        data = [("test1", "test2"), ("test3", "test4")]
        col_names = ["col1", "col2"]
        result = format_query_output(data, col_names)
        assert result == [{"col1": "test1", "col2": "test2"}, {"col1": "test3", "col2": "test4"}]


class TestSelectActivityData:
    def test_select_activity_data_default_value_arguments(self):
        user_id = 1
        result = select_activity_data(user_id)
        assert len(result) > 1
        assert isinstance(result, list)
        for item in result:
            assert isinstance(item, dict)
            assert isinstance(item["id"], int)
            assert isinstance(item["distance_km"], float)
            assert isinstance(item["moving_time"], str)

    def test_select_activity_data_date_range(self):
        #testing seeded data, assuming no more data added between the given dates
        user_id = 1
        date_start = "2025/02/01"
        date_end = "2025/02/14"
        result = select_activity_data(user_id, date_start, date_end)
        assert len(result) == 2
        assert result[0]["id"] == 9
        assert result[0]['distance_km'] == 5.59
        assert result[0]['moving_time'] == '00:38:57'
        assert result[0]['date'] == '2025/02/10'