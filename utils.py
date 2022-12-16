import json
import pickle

from selenium import webdriver

quotes_path = 'answers/quotes.json'
description_path = 'answers/descriptions.json'


def save_cookies(driver: webdriver.Chrome, cookies_path):
    with open(cookies_path, 'wb') as filehandler:
        print(driver.get_cookies())
        pickle.dump(driver.get_cookies(), filehandler)


def load_cookies(driver: webdriver.Chrome, cookies_path):
    with open(cookies_path, 'rb') as cookies_file:
        cookies = pickle.load(cookies_file)
        for cookie in cookies:
            driver.add_cookie(cookie)


def load_quotes_answers() -> dict:
    with open(quotes_path, 'r', encoding='utf-8') as js_file:
        res = json.load(js_file)
    return res


def save_quotes_answers(answers):
    with open(quotes_path, 'w', encoding='utf-8') as js_file:
        json.dump(answers, js_file, ensure_ascii=False, indent=2)


def load_description_answers() -> dict:
    with open(description_path, 'r', encoding='utf-8') as js_file:
        res = json.load(js_file)
    return res


def save_description_answers(answers):
    with open(description_path, 'w', encoding='utf-8') as js_file:
        json.dump(answers, js_file, ensure_ascii=False, indent=2)
