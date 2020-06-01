import sys
import os
import platform
import random
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains


class kuisioner(object):
    def __init__(self, username, password):
        self.options = Options()
        self.options.headless = False
        self.options.add_argument("--window-size=1366x768")
        self.driver = webdriver.Firefox(options=self.options)
        self.username = username
        self.password = password

    def wait(self, xpath, message, timeout=15):
        timeout = timeout
        try:
            element_present = EC.presence_of_element_located(
                (By.XPATH, xpath))
            WebDriverWait(self.driver, timeout).until(element_present)
        except TimeoutException:
            print("Timed out waiting for {} loaded".format(message))
            self.driver.quit()
            sys.exit(1)

    def login(self):
        print("Login Start")
        self.driver.get('http://ujian.jti.polinema.ac.id/')

        username_input = '//*[@id="xuser_name"]'
        password_input = '//*[@id="xuser_password"]'
        login_submit = '//*[@id="login"]'

        self.wait(xpath=username_input, message="username input")

        self.driver.find_element_by_xpath(
            username_input).send_keys(self.username)
        self.driver.find_element_by_xpath(
            password_input).send_keys(self.password)
        self.driver.find_element_by_xpath(login_submit).click()

        list_test = '/html/body/div[3]/div/div[1]/table'

        self.wait(xpath=list_test, message="home page")
        print("Login Completed")

    def get_remaining(self):
        return self.driver.find_elements_by_link_text('kerjakan')

    def kuis(self):
        print("Questionnaire Start")
        action_remaining = self.get_remaining()
        if len(action_remaining) == 0:
            print("All Questionnaire already complete")
            sys.exit(1)
        else:
            print("List Questionnaire remaining")
        forward_td = []
        for i in range(len(action_remaining)):
            temp_backward = action_remaining[i].find_element_by_xpath(
                '../..')
            forward_td.append(
                temp_backward.find_element_by_xpath('td[1]/strong/a').text)
            print(forward_td[i])

        answer_area = '//*[@id="answertext"]'
        confirmed_btn = '//*[@id="confirmanswer"]'
        next_btn = '//*[@id="nextquestion"]'
        end_btn = '//*[@id="terminatetest"]'
        confirm_end_btn = '//*[@id="forceterminate"]'

        print("Begin completing all Questionnaire job")
        for i in range(len(action_remaining)):
            action_remaining = self.get_remaining()
            print("Start completing {}".format(forward_td[i]))
            action_remaining[0].click()

            btn_start = '/html/body/div[3]/div/div[3]/a[1]'
            self.wait(xpath=btn_start, message="Start Button Questionnaire")
            lala = 0
            self.driver.find_element_by_xpath(btn_start).click()
            for j in range(22):
                self.wait(xpath=answer_area, message="answer area")
                element_answer = self.driver.find_element_by_xpath(answer_area)
                element_answer.clear()
                element_answer.send_keys(random.randint(2, 5))
                self.driver.find_element_by_xpath(confirmed_btn).click()
                self.driver.find_element_by_xpath(next_btn).click()

            self.driver.find_element_by_xpath(end_btn).click()

            self.wait(xpath=confirm_end_btn, message="confirm end")

            self.driver.find_element_by_xpath(confirm_end_btn).click()
            print("job completed")
        print("All Questionnaire completed")
