#!python3

from selenium import webdriver as web
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from pathlib import Path
import json
import requests
from urllib.parse import quote
from datetime import datetime as date

HOME_DIR = str(Path.home())

def write_response_to_file(resp):
    rcfile = open(HOME_DIR + '/.facebookclirc', 'w')
    data = json.dumps(resp)
    rcfile.write(data)
    rcfile.close()


def check_for_rc_file():
    if Path(HOME_DIR + '/.facebookclirc').is_file():
        try:
            tmp = open(HOME_DIR + '/.facebookclirc', 'r')
            data = json.loads(tmp.read())
            tmp.close()
            if date.now().timestamp() - float(data['now']) < float(data['expires_in']):
                return True
            else:
                return False
        except Exception:
            return False

    return False


def log_user_in():    
    # Start a chrome session
    chrome = web.Chrome()

    # Define the url for login flow
    url = 'https://www.facebook.com/v3.2/dialog/oauth?'
    url += 'client_id=' + config['app_id'] + '&redirect_uri=' + config['redirect_uri']
    url += '&state={"{st=state123abc,ds=123456789}"}'
    # url = 'https://graph.facebook.com/oauth/authorize?client_id=1317068665099061&redirect_uri=https://www.facebook.com/connect/login_success.html'
    
    # Launch the url into the browser window
    chrome.get(url)

    # Declare a var to store the final url
    final_url = []

    # Wait for the user to successfully log in
    try:
        wait = WebDriverWait(chrome, 600)
        wait.until(lambda d: config['redirect_uri'] in chrome.current_url)

    except TimeoutException:
        print ('Failed to log in withing specified time: 10 minutes')
        exit(1)

    finally:
        final_url.append(chrome.current_url)

        # Close the browser window
        chrome.close()


    # Extract the code from the redirect uri of facebook
    if '?code=' in final_url[0]:
        code = final_url[0][final_url[0].index('?code=') + 6:final_url[0].index('&state')]

    # print (code)

    def get_access_token_from_code():
        req_data = '?client_id={}&redirect_uri={}&client_secret={}&code={}'.format(\
                config['app_id'], \
                quote(config['redirect_uri'], safe=''), \
                config['app_secret'], \
                code
            )
        # print (req_data)
        response = requests.get('https://graph.facebook.com/v3.2/oauth/access_token' + req_data)
        return response

    resp = get_access_token_from_code().json()
    resp['now'] = str(date.now().timestamp())
    write_response_to_file(resp)

config = None

def init():
    def read_config_file():
        global config
        try:
            cfgfile = open('../fbconfig.json', 'r')
            config = json.loads(cfgfile.read())

        except Exception:
            print ('Damn! Something fishy\n Try re-installing facebook-cli')
            exit(1)
        
    read_config_file()

    if not check_for_rc_file():
        # User is not logged into Facebook
        # Log him in first
        log_user_in()


if __name__ == "__main__":
    init()

