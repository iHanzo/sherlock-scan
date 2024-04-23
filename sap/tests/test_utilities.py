import sys
sys.path.append('/home/parrot/fyp/fds/sap')
import unittest
import os
from unittest.mock import mock_open, patch
from sap import read_lines_from_file

class TestSAPFunctions(unittest.TestCase):
    def test_read_lines_from_file(self):
        expected_output = ['line1', 'line2', 'line3']
        result = read_lines_from_file('path/to/testfile.txt')
        self.assertEqual(result, expected_output)

if __name__ == '__main__':
    unittest.main()

class TestUtilityFunctions(unittest.TestCase):
    def test_read_lines_from_file(self):
        # This test will check if the function correctly reads lines from a file.
        expected_result = ['user1', 'user2', 'user3']
        with open('test_usernames.txt', 'w') as file:
            file.write("\n".join(expected_result))
        
        result = read_lines_from_file('test_usernames.txt')
        self.assertEqual(result, expected_result)

    def test_set_headers_same_for_all(self):
        # Test that set_headers returns the same headers for any input if the mode is 'same_for_all'
        header_values_list = [{'User-Agent': 'TestAgent', 'Accept': 'text/html'}]
        header_mode = 'same_for_all'
        expected_headers = {'User-Agent': 'TestAgent', 'Accept': 'text/html'}

        result = set_headers(header_mode, header_values_list, 'username', ['user1', 'user2'])
        self.assertEqual(result, expected_headers)

    def test_set_headers_unique_per_user(self):
        # Test that set_headers returns unique headers based on the username index
        header_values_list = [
            {'User-Agent': 'User1Agent', 'Accept': 'application/json'},
            {'User-Agent': 'User2Agent', 'Accept': 'text/html'}
        ]
        header_mode = 'unique_headers_per_username'
        usernames = ['user1', 'user2']

        result = set_headers(header_mode, header_values_list, 'user1', usernames)
        expected_headers = {'User-Agent': 'User1Agent', 'Accept': 'application/json'}
        self.assertEqual(result, expected_headers)

    def test_delay_handling_minimum_delay(self):
        # Test minimum delay handling when only the minimum delay is set
        min_delay = 1.0
        max_delay = 1.0
        result = calculate_delay(min_delay, max_delay)
        self.assertEqual(result, 1.0)

    def test_delay_handling_random_delay_within_range(self):
        # Test that the delay is within the specified range
        min_delay = 1.0
        max_delay = 2.0
        result = calculate_delay(min_delay, max_delay)
        self.assertTrue(min_delay <= result <= max_delay)

    def test_delay_handling_invalid_range(self):
        # Test handling of an invalid range where min_delay is greater than max_delay
        min_delay = 3.0
        max_delay = 2.0
        with self.assertRaises(ValueError):
            calculate_delay(min_delay, max_delay)

    def test_read_lines_from_file(self):
        # Test reading lines from a file
        with open('test_usernames.txt', 'w') as file:
            file.write("user1\nuser2\nuser3")
        result = read_lines_from_file('test_usernames.txt')
        self.assertEqual(result, ["user1", "user2", "user3"])
        os.remove('test_usernames.txt')

    def test_read_header_values(self):
        # Test reading header values from a CSV file
        with open('test_headers.csv', 'w') as file:
            file.write("header1,header2\nvalue1,value2\nvalue3,value4")
        result = read_header_values('test_headers.csv')
        expected = [{'header1': 'value1', 'header2': 'value2'}, {'header1': 'value3', 'header2': 'value4'}]
        self.assertEqual(result, expected)
        os.remove('test_headers.csv')

    def test_attempt_login_success(self):
        # Setup a requests session with a mock server that simulates a successful login
        with requests_mock.Mocker() as m:
            m.post("http://testserver/login", text="Welcome to the Home Page")
            session = requests.Session()
            success = attempt_login(session, "http://testserver/login", "testuser", "password", {'User-Agent': 'test'}, "csrf_token")
            self.assertTrue(success)

    def test_attempt_login_failure(self):
        # Setup to simulate a failed login attempt
        with requests_mock.Mocker() as m:
            m.post("http://testserver/login", text="Login Failed")
            session = requests.Session()
            success = attempt_login(session, "http://testserver/login", "testuser", "wrongpassword", {'User-Agent': 'test'}, "csrf_token")
            self.assertFalse(success)

def test_set_headers_same_for_all(self):
    header_values_list = [{'User-Agent': 'UA-Test', 'Accept': 'text/html'}]
    headers = set_headers('same_for_all', header_values_list, 'testuser', ['testuser'])
    self.assertEqual(headers, {'User-Agent': 'UA-Test', 'Accept': 'text/html'})

def test_set_headers_per_username(self):
    header_values_list = [{'User-Agent': 'UA-Test1'}, {'User-Agent': 'UA-Test2'}]
    headers = set_headers('per_username', header_values_list, 'testuser', ['testuser', 'anotheruser'])
    self.assertEqual(headers, {'User-Agent': 'UA-Test1'})

def test_set_headers_random_combination(self):
    header_values_list = [{'User-Agent': 'UA-Test1'}, {'User-Agent': 'UA-Test2'}]
    random.seed(0)  # Setting seed to make the test predictable
    headers = set_headers('random_combination', header_values_list, 'testuser', ['testuser'])
    self.assertIn(headers['User-Agent'], ['UA-Test1', 'UA-Test2'])

def test_read_header_values_empty_file(self):
    with patch('builtins.open', mock_open(read_data="")) as mocked_file:
        result = read_header_values('dummy_path.csv')
        self.assertEqual(result, [])
        mocked_file.assert_called_once_with('dummy_path.csv', newline='')

def test_read_header_values_non_empty_file(self):
    csv_content = "User-Agent,Accept\nMozilla/5.0,text/html"
    expected_result = [{'User-Agent': 'Mozilla/5.0', 'Accept': 'text/html'}]
    with patch('builtins.open', mock_open(read_data=csv_content)) as mocked_file:
        result = read_header_values('dummy_path.csv')
        self.assertEqual(result, expected_result)
        mocked_file.assert_called_once_with('dummy_path.csv', newline='')

def test_set_headers_uniform(self):
    header_values_list = [{'User-Agent': 'TestAgent', 'Accept': 'text/html'}]
    result = set_headers('same_for_all', header_values_list, 'user1', ['user1', 'user2'])
    self.assertEqual(result, {'User-Agent': 'TestAgent', 'Accept': 'text/html', 'X-Forwarded-For': '127.0.0.1'})

def test_set_headers_random(self):
    header_values_list = [{'User-Agent': 'Agent1', 'Accept': 'application/json'}, {'User-Agent': 'Agent2', 'Accept': 'text/plain'}]
    with patch('random.choice', return_value=header_values_list[1]):
        result = set_headers('random_headers_each_request', header_values_list, 'user1', ['user1', 'user2'])
        self.assertEqual(result, {'User-Agent': 'Agent2', 'Accept': 'text/plain', 'X-Forwarded-For': '127.0.0.1'})

def test_set_headers_per_user(self):
    header_values_list = [{'User-Agent': 'Agent1', 'Accept': 'application/json'}, {'User-Agent': 'Agent2', 'Accept': 'text/plain'}]
    result = set_headers('unique_headers_per_username', header_values_list, 'user2', ['user1', 'user2'])
    self.assertEqual(result, {'User-Agent': 'Agent2', 'Accept': 'text/plain', 'X-Forwarded-For': '127.0.0.1'})

def test_read_lines_from_file_valid(self):
    mock_open = mock.mock_open(read_data='user1\nuser2\nuser3')
    with mock.patch('builtins.open', mock_open):
        result = read_lines_from_file('dummy_path.txt')
        self.assertEqual(result, ['user1', 'user2', 'user3'])

def test_read_header_values(self):
    header_csv_content = 'User-Agent,Accept\nBrowser1,text/html\nBrowser2,application/json'
    mock_open = mock.mock_open(read_data=header_csv_content)
    with mock.patch('builtins.open', mock_open):
        with mock.patch('csv.DictReader', return_value=[{'User-Agent': 'Browser1', 'Accept': 'text/html'}, {'User-Agent': 'Browser2', 'Accept': 'application/json'}]):
            result = read_header_values('dummy_path.csv')
            self.assertEqual(result, [{'User-Agent': 'Browser1', 'Accept': 'text/html'}, {'User-Agent': 'Browser2', 'Accept': 'application/json'}])

def test_read_lines_from_file_empty(self):
    mock_open = mock.mock_open(read_data='')
    with mock.patch('builtins.open', mock_open):
        result = read_lines_from_file('dummy_path.txt')
        self.assertEqual(result, [])

def test_select_file(self):
    mock_filedialog = mock.Mock()
    mock_filedialog.askopenfilename.return_value = '/path/to/file.txt'
    with mock.patch('tkinter.filedialog', mock_filedialog):
        entry_widget = mock.Mock()
        select_file(entry_widget)
        entry_widget.delete.assert_called_once_with(0, 'end')
        entry_widget.insert.assert_called_once_with(0, '/path/to/file.txt')

def test_reset_buttons(self):
    start_button = mock.Mock()
    cancel_button = mock.Mock()
    reset_buttons(start_button, cancel_button)
    start_button.config.assert_called_once_with(state='normal')
    cancel_button.config.assert_called_once_with(state='disabled')

def test_reload_script(self):
    mock_os = mock.Mock()
    mock_sys = mock.Mock()
    with mock.patch('os.execl', mock_os), mock.patch('sys.executable', 'python'), mock.patch('sys.argv', ['app.py']):
        reload_script()
        mock_os.assert_called_once_with('python', 'python', 'app.py')
