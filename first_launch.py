from selenium import webdriver
from config import url
from selenium.webdriver.common.by import By

from bot import sleep
from config import cookies_path
from utils import save_cookies


def get_access_to_account():
    with open('account.txt', 'r', encoding='utf-8') as f:
        login, password = f.readlines()

    driver = webdriver.Chrome()
    driver.get(url)
    sleep()
    assert 'Угадывайте' in driver.title
    sleep()
    login_button = driver.find_element(by=By.CLASS_NAME, value='header__button')
    login_button.click()
    login_input = driver.find_element(by=By.CLASS_NAME, value='Textinput-Control')
    sleep()
    login_input.send_keys(login)
    sleep()
    login_input = driver.find_element(by=By.CLASS_NAME, value='Textinput-Control')
    login_input.send_keys(password)
    login_button = driver.find_element(by=By.ID, value='passp:sign-in')
    login_button.click()
    sleep()
    sleep()
    sleep()
    sleep()
    sleep()
    sleep()
    sleep()
    sleep()
    sleep()
    sleep()
    sleep()
    sleep()
    sleep()
    sleep()
    sleep()
    sleep()
    sleep()
    sleep()
    sleep()
    sleep()
    sleep()
    sleep()
    save_cookies(driver, cookies_path)
    print('Successfully saved cookies!')


if __name__ == '__main__':
    get_access_to_account()
