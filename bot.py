import time

from selenium.webdriver.common.by import By

from config import url, cookies_path
from utils import *

from random import random


def wait(function):
    def wrapper(self):
        sleep()
        function(self)

    return wrapper


def sleep():
    a = 1 + random()
    time.sleep(a)


class Bot:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.url = url
        self.quotes_answers = load_quotes_answers()
        self.description_answers = load_description_answers()

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
        counter = 0
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
                    counter += 1
                    print(f'Current Score: {counter}')
                    sleep()
                    button.click()
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
                    counter += 1
                    lives += 1
                    print(f'Current Score: {counter}')

                if lives > 0:
                    print(f'Has {lives} lives')
                    try:
                        continue_button = self.driver.find_element(by=By.CLASS_NAME, value='button_color_darken')
                        continue_button.click()
                    except Exception as e:
                        print('Cant find the continue button')
                else:
                    print('Run out of lives')
                    print(f'Final Score: {counter}')
                    lives = 3
                    counter = 0
                    sleep()
                    again_button = self.driver.find_element(by=By.CLASS_NAME, value='button_color_white-2')
                    again_button.click()

    def run_game_descriptions(self):
        sleep()
        category_button = [i for i in self.driver.find_elements(by=By.CLASS_NAME, value='episode-card__title') if
                           i.text == 'Описания'][0]
        category_button.click()
        sleep()
        run_button = [button for button in self.driver.find_elements(by=By.TAG_NAME,
                                                                     value='button') if button.text == 'Начать игру'][0]
        run_button.click()

        lives = 3
        counter = 0
        while True:
            sleep()

            is_random_answer = False
            print('-------')
            question_label = self.driver.find_element(by=By.CLASS_NAME, value='game__test-question').text
            print(question_label)
            sleep()
            answers_buttons = self.driver.find_elements(by=By.CLASS_NAME, value='text-fit')
            my_answer = [self.description_answers[key] for key in self.description_answers if
                         key == question_label]
            if my_answer:
                print('Has answer')
                my_answer = my_answer[0]
            for button in answers_buttons:
                if button.text == my_answer:
                    counter += 1
                    print(button.text)
                    button.click()
                    break
            else:
                print('Random')
                is_random_answer = True
                button = answers_buttons[0]
                button_text = button.text
                print(button.text)
                button.click()
                time.sleep(1)

            try:
                sleep()
                right_answer = self.driver.find_element(by=By.CLASS_NAME, value='modal-wrong-answer__title').text
                print(right_answer)
                right_answer = right_answer[right_answer.find('«') + 1:right_answer.rfind('»')]
                lives -= 1
                print('-')
                print(question_label)
                print('-')
                print(self.description_answers.get(question_label))
                self.description_answers[question_label] = right_answer
                print(self.description_answers.get(question_label))
                print('-')
                save_description_answers(self.description_answers)
                sleep()
                continue_button = self.driver.find_element(by=By.CLASS_NAME, value='button_color_darken')
                continue_button.click()
            except Exception as e:
                if is_random_answer:
                    print('-')
                    print(question_label)
                    print('-')
                    print(self.description_answers.get(question_label))
                    self.description_answers[question_label] = button_text
                    print(self.description_answers.get(question_label))
                    print('-')
                    save_description_answers(self.description_answers)
                print(f'Current Score: {counter}')

            if lives > 0:
                print(f'Has {lives} lives')
            else:
                print('Run out of lives')
                print(f'Final Score: {counter}')
                lives = 3
                counter = 0
                sleep()
                again_buttons = self.driver.find_elements(by=By.TAG_NAME, value='button')
                [button for button in again_buttons if button.text == 'Играть ещё раз'][0].click()
            print('-------')

    def run(self, game_type):
        self.setup()
        self.authorisation()
        if game_type == 1:
            self.run_game_quotes()  # Игра - цитаты
        elif game_type == 2:
            self.run_game_descriptions()  # Игра - описания

        sleep()
        self.driver.close()


def main():
    bot = Bot()
    while True:
        try:
            # 1 - Игра - Цитаты
            # 2 - Игра - Описания
            bot.run(1)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    main()
