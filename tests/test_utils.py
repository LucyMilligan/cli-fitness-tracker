from visualisation.utils import get_dates, get_user_id, is_valid_date, plot_activity_input, plot_all_activity_data, exit
import pytest

# main script (using these utils) is manually tested with different scenarios

class TestGetUserId:
    def test_get_user_id_returns_user_id(self, mocker):
        input_mock = mocker.patch("builtins.input")
        input_mock.return_value = "1"

        result = get_user_id()

        assert result == "1"


class TestPlotAllActivityData:
    def test_plot_all_activity_data_returns_true(self, mocker):
        input_mock = mocker.patch("builtins.input")
        input_mock.return_value = "y"

        result = plot_all_activity_data()

        assert result == True

    def test_plot_all_activity_data_returns_false(self, mocker):
        input_mock = mocker.patch("builtins.input")
        input_mock.return_value = "N"

        result = plot_all_activity_data()

        assert result == False

    def test_plot_all_activity_data_returns_string_for_invalid_input(self, mocker):
        input_mock = mocker.patch("builtins.input")
        input_mock.return_value = "yes"

        result = plot_all_activity_data()

        assert result == "Invalid input"

class TestIsValidDate:
    def test_is_valid_date_returns_true_for_valid_date_and_format(self):
        date = "2025/03/30"
        result = is_valid_date(date)
        assert result == True


    def test_is_valid_date_returns_false_for_invalid_format(self):
        date1 = "2025-03-30"
        date2 = "03 March 2025"
        result1 = is_valid_date(date1)
        result2 = is_valid_date(date2)
        assert result1 == False
        assert result2 == False


    def test_is_valid_date_returns_false_for_month_day_incorrect(self):
        date = "2025/30/03"
        result = is_valid_date(date)
        assert result == False


class TestGetDates:
    def test_get_dates_returns_dates_as_tuple(self, mocker):
        #mock user input (same user input for start and end date)
        input_mock_1 = mocker.patch("builtins.input")
        input_mock_1.return_value = "2025/03/20"

        result = get_dates()
        assert result == ("2025/03/20", "2025/03/20")
        

class TestPlotActivityInput:
    def test_plot_activity_input_returns_input(self, mocker):
        input_mock = mocker.patch("builtins.input")
        input_mock.return_value = "a"

        result = plot_activity_input()

        assert result == "a"

class TestExit:
    def test_exit_quits_program_with_message(self):
        with pytest.raises(SystemExit) as e:
            exit()
        assert e.value.code == "Goodbye! Enjoy your next activity!"


####### if wanting to patch a function and get the call count #######
    # def test_get_user_id_calls_func_again_if_incorrect_input(mocker):
    #     #mock incorrect input
    #     input_mock = mocker.patch("builtins.input")
    #     input_mock.return_value = "a"

    #     #mock get_user_id function (that will be called inside the function)
    #     func_mock = mocker.patch("visualisation.utils.get_user_id")

    #     get_user_id()

    #     #assert that the get_user_id is called in the else block 
    #     #(should be 0 if input is correct)
    #     assert func_mock.call_count == 1