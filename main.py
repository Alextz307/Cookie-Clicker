from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
import os
import time

CHROME_DRIVER_PATH = os.environ.get('CHROME_DRIVER_PATH')
URL = 'http://orteil.dashnet.org/experiments/cookie/'

DELTA_TIME = 300
DELTA_UPGRADE = 7

service = Service(executable_path=CHROME_DRIVER_PATH)
driver = webdriver.Chrome(service=service)

driver.get(url=URL)

store = driver.find_elements(By.CSS_SELECTOR, '#store div')
store.pop()
store.pop()
store.pop(-2)
store.reverse()

items = [item.get_attribute('id') for item in store]

cookie = driver.find_element(by='id', value='cookie')
balance_element = driver.find_element(by='id', value='money')

last_time = time.time()
start_time = time.time()


def try_item(item_id):
    price_element = driver.find_element(By.CSS_SELECTOR, f'#{item_id} b')

    price = int(price_element.text.split('-')[1].strip().replace(',', ''))
    balance = int(balance_element.text.replace(',', ''))

    if price <= balance:
        driver.find_element(by='id', value=item_id).click()
        return True

    return False


while time.time() <= start_time + DELTA_TIME:
    cookie.click()

    if last_time + DELTA_UPGRADE <= time.time():
        for item in items:
            try:
                try_item(item)
            except StaleElementReferenceException:
                pass

        last_time = time.time()


cookies_per_second = driver.find_element(by='id', value='cps')
print(cookies_per_second.text)

driver.quit()
