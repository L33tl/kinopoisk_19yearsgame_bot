import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()
driver.get('https://www.python.org')
assert 'Python' in driver.title
elem = driver.find_element(value="q", by=By.NAME)
elem.send_keys('pycon')
elem.send_keys(Keys.RETURN)
assert 'No results found.' not in driver.page_source
time.sleep(2)
driver.close()
