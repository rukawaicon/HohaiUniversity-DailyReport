import requests
import json
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions
from os import makedirs
from os.path import exists
import time
# from urllib.parse import urljoin

BASE_URL = 'http://authserver.hhu.edu.cn/authserver/login?service=http%3A%2F%2Fdailyreport.hhu.edu.cn%2Fpdc%2Fform%2Flist'
INDEX_URL = 'http://dailyreport.hhu.edu.cn/pdc/formDesignApi/S/gUTwwojq'
HISTORY_URL = 'http://dailyreport.hhu.edu.cn/pdc/formDesign/showFormFilled?selfFormWid=A335B048C8456F75E0538101600A6A04&lwUserId=1808080116'

USERAGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36'
USERNAME = '6'
PASSWORD = ''

# response_login = requests.post(BASE_URL, data={
#     'username': USERNAME,
#     'password': PASSWORD
# }, headers = {
#    'User-Agent': USERAGENT
# }, allow_redirects=False)
#
# cookies = response_login.cookies
# print('Cookies:', cookies)

# response_index = requests.get(INDEX_URL, cookies=cookies)
option = ChromeOptions()
option.add_argument('--headless')

browser = webdriver.Chrome(options=option)
browser.set_window_size(1366, 768)
browser.get(BASE_URL)
browser.find_element(By.ID, 'username').send_keys(USERNAME)
browser.find_element(By.ID, 'password').send_keys(PASSWORD)
browser.find_element(By.CSS_SELECTOR, 'button[class="auth_login_btn primary full_width"]').click()
# time.sleep(10)

cookies = browser.get_cookies()
button = browser.find_element(By.CSS_SELECTOR, 'a[class="datav-flex "]')
button.click()
button1 = browser.find_element(By.ID, 'saveBtn')
button1.click()
browser.close()

session = requests.Session()
for cookie in cookies:
    session.cookies.set(cookie['name'], cookie['value'])
response_history = session.get(HISTORY_URL)
html = response_history.text
print('Response Status:', response_history.status_code)
# print(html)
soup = BeautifulSoup(html, 'lxml')
data = soup.select_one('table tr')
print(data)

RESULTS_DIR = 'results'
exists(RESULTS_DIR) or makedirs(RESULTS_DIR)
data_path = f'{RESULTS_DIR}/reports_results.csv'
# f = open(data_path, 'w', encoding='utf-8')
# f.write(data)
# f.close()
dp = pd.DataFrame(data)
dp.to_csv(data_path, header=False, index=False)

