#!python3

from selenium import webdriver as web
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from pathlib import Path
import json

HOME_DIR = str(Path.home())

def write_access_toke_to_file(access_token):
    rcfile = open(HOME_DIR + '/.facebookclirc', 'w')
    data = {}
    data['access_token'] = access_token
    data = json.dumps(data)
    rcfile.write(data)
    rcfile.close()


def check_for_rc_file():
    if Path(HOME_DIR + '/.facebookclirc').is_file():
        return True
    return False


def log_user_in():    
    # Start a chrome session
    chrome = web.Chrome()

    # Define the url for login flow
    url = 'https://www.facebook.com/v3.2/dialog/oauth?'
    url += 'client_id=1317068665099061&redirect_uri=https://www.facebook.com/connect/login_success.html&' 
    url += 'state={"{st=state123abc,ds=123456789}"}'
    # url = 'https://graph.facebook.com/oauth/authorize?client_id=1317068665099061&redirect_uri=https://www.facebook.com/connect/login_success.html'
    
    # Launch the url into the browser window
    chrome.get(url)

    # Wait for the user to successfully log in
    try:
        wait = WebDriverWait(chrome, 600)
        wait.until(lambda d: 'https://www.facebook.com/connect/login_success.html' in chrome.current_url)

    except TimeoutException:
        print('Failed to log in withing specified time: 10 minutes')
        exit(1)

    finally:
        # Close the browser window
        chrome.close()

    # Capture the url containing access token
    final_url = chrome.current_url

    # Extract the access token from the redirect uri of facebook
    if '?code=' in final_url:
        code = final_url[final_url.index('?code=') + 6:final_url.index('&state')]

        # Write the access token to a file for future use
        write_access_toke_to_file(code)


def init():
    if not check_for_rc_file():
        # User is not logged into Facebook
        # Log him in first
        log_user_in()


if __name__ == "__main__":
    init()

    