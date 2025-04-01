from visualisation.plots_utils import calculate_pace_mins_per_km, calculate_time_secs, convert_pace_to_float, create_dataframe, format_query_output, select_activity_data
import pandas as pd

#visual test for plots done manually at the moment
#note - currently happy path testing

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


class TestCalculatePace:
    def test_calculate_pace_min_per_km_30_mins(self):
        moving_time = "00:30:00"
        distance = 5.0
        expected = "6:00"
        result = calculate_pace_mins_per_km(distance, moving_time)
        assert result == expected

    def test_calculate_pace_min_per_km_33_mins(self):
        moving_time = "00:33:00"
        distance = 5.0
        expected = "6:36"
        result = calculate_pace_mins_per_km(distance, moving_time)
        assert result == expected
    
    def test_calculate_pace_min_per_km_greater_than_10_mins_per_km(self):
        moving_time = "02:15:30"
        distance = 5.0
        expected = "27:06"
        result = calculate_pace_mins_per_km(distance, moving_time)
        assert result == expected


class TestConvertPaceToFloat:
    def test_convert_pace_to_float(self):
        pace_string = "6:53"
        result = convert_pace_to_float(pace_string)
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
        date_start = "2025/02/09"
        date_end = "2025/02/11"
        result = select_activity_data(user_id, date_start, date_end)
        assert result[0]["id"] == 9
        assert result[0]['distance_km'] == 5.59
        assert result[0]['moving_time'] == '00:38:57'
        assert result[0]['date'] == '2025/02/10'


class TestCreateDataframe:
    def test_create_dataframe_creates_a_dataframe(self):
        data = [{"date": "2025/02/25", "distance_km": 5.0, "moving_time":"00:30:00"}, 
                {"date": "2025/02/24", "distance_km": 1.0, "moving_time":"00:07:00"}]
        expected_df = pd.DataFrame({"date": ["2025/02/25", "2025/02/24"],
                                   "distance_km": [5.0, 1.0],
                                   "moving_time": ["00:30:00", "00:07:00"],
                                   "pace": ["6:00", "7:00"],
                                   "pace_numeric": [6.00, 7.00]})
        expected_df["date"] = pd.to_datetime(expected_df["date"], format="%Y/%m/%d")
        result = create_dataframe(data)
        pd.testing.assert_frame_equal(expected_df, result)

    def test_create_dataframe_dates_incorrect_format(self):
        data = [{"date": "2025-02-25", "distance_km": 5.0, "moving_time":"00:30:00"}, 
                {"date": "March 25th 25", "distance_km": 1.0, "moving_time":"00:07:00"}]
        expected_df = pd.DataFrame({"date": ["NaT", "NaT"],
                                   "distance_km": [5.0, 1.0],
                                   "moving_time": ["00:30:00", "00:07:00"],
                                   "pace": ["6:00", "7:00"],
                                   "pace_numeric": [6.00, 7.00]})
        expected_df["date"] = pd.to_datetime(expected_df["date"], format="%Y/%m/%d")
        result = create_dataframe(data)
        pd.testing.assert_frame_equal(expected_df, result)