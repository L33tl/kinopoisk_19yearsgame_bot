import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from config import url, cookies_path
from utils import *

from random import random, randint


def wait(function):
    def wrapper(self):
        sleep()
        function(self)

    return wrapper


def sleep():
    a = (randint(1, 2) if randint(0, 1) else randint(4, 5)) + random()
    print(a)
    time.sleep(a)


class Bot:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.url = url
        self.quotes_answers = load_quotes_answers()

    def setup(self):
        self.driver.set_window_position(1920 / 2, 0)
        self.driver.get(self.url)
        assert 'Угадывайте' in self.driver.title

    def authorisation(self):
        load_cookies(self.driver, cookies_path)
        self.driver.refresh()

    @wait
    def run_game_quotes(self):
        category_button = [i for i in self.driver.find_elements(by=By.CLASS_NAME, value='episode-card__title') if
                           i.text == 'Цитаты'][0]
        category_button.click()
        sleep()
        run_button = [button for button in self.driver.find_elements(by=By.TAG_NAME,
                                                                     value='button') if button.text == 'Начать игру'][0]
        run_button.click()

        lives = 3
        while True:
            sleep()
            question_label = self.driver.find_element(by=By.CLASS_NAME, value='game__test-question')
            right_answer = [self.quotes_answers[key] for key in self.quotes_answers if key == question_label.text]
            if right_answer:
                right_answer = right_answer[0]

            answers_buttons = self.driver.find_elements(by=By.CLASS_NAME, value='text-fit')
            for button in answers_buttons:
                if button.text == right_answer:
                    print('Has answer')
                    button.click()
                    sleep()
                    break
            else:
                print('Random')
                lives -= 1
                button.click()
                sleep()
                try:
                    right_answer = self.driver.find_element(by=By.CLASS_NAME, value='modal-wrong-answer__title').text
                    right_answer = right_answer[right_answer.find('«') + 1:right_answer.find('»')]
                    self.quotes_answers[question_label.text] = right_answer
                    save_quotes_answers(self.quotes_answers)
                except Exception as e:
                    print(123123)
                    lives += 1
                    # print(e)

                if lives > 0:
                    print(f'Has {lives} lives')
                    try:
                        continue_button = self.driver.find_element(by=By.CLASS_NAME, value='button_color_darken')
                        continue_button.click()
                    except Exception as e:
                        print('Cant find the continue button')
                else:
                    print('Run out of lives')
                    lives = 3
                    sleep()
                    again_button = self.driver.find_element(by=By.CLASS_NAME, value='button_color_white-2')
                    again_button.click()

    def run(self):
        self.setup()
        self.authorisation()
        self.run_game_quotes()

        sleep()
        self.driver.close()


def main():
    bot = Bot()
    while True:
        try:
            bot.run()
        except Exception as e:
            print(e)


if __name__ == '__main__':
    main()
