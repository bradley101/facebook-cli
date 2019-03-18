#!python3

from selenium import webdriver as web
from selenium.webdriver.support.ui import WebDriverWait

chrome = web.Chrome()
# url = 'https://www.facebook.com/v3.2/dialog/oauth?client_id=1317068665099061&redirect_uri=https://www.facebook.com/connect/login_success.html&state={"{st=state123abc,ds=123456789}"}'
url = 'https://graph.facebook.com/oauth/authorize?client_id=1317068665099061&redirect_uri=https://www.facebook.com/connect/login_success.html'
chrome.get(url)
wait = WebDriverWait(chrome, 60)
wait.until(lambda d: 'https://www.facebook.com/connect/login_success.html' in chrome.current_url)
print (chrome.current_url)
chrome.close()

# print (a)
# https://www.facebook.com/connect/login_success.html?code=AQA83rdZ381DrzsrBIvsoaGGoCkGbISbxVujYIBVyXbzZTHZYYQC8upeERjP1iKGvSx_OSwtoaJGZwP9QnnwGfYtYFD-6ntDCd2xQ3-qJiCEVzxBgG43mI9_P4Sd3-Lnudr5UngQXTDvoXwaPIP0XxUF0O8DcGOu6Up6PX-BcKIP-1ZUIYeJ9Dc8-FyL5YaCvpytdtGJoVTuFAcJD8SvifnndCDoJdjmOtWGaKVugArCdJjG-cwbmHECSwPtHpdLBAEb6DZxQhrrkY_EJKbANFfWJEwPGkstNyZV95dbpvVHWbZdcmTRJLZvpUN1f3PyNH_wDD7GzzLHsgnxc_ZTcLWR#_=_
