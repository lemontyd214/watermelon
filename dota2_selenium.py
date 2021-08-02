from selenium import webdriver
import time
import json

driver = webdriver.Chrome()


def init():
    driver.maximize_window()
    driver.get("https://www.ixigua.com/")

    time.sleep(5)


def login():
    login_btn = driver.find_element_by_class_name("loginButton")
    login_btn.click()

    time.sleep(0.5)

    switch = driver.find_element_by_id("sso_pwd_login")
    switch.click()

    time.sleep(0.5)

    username = driver.find_element_by_name("username").send_keys(14701021843)
    pwd = driver.find_element_by_name("password").send_keys("ty1994214")
    login_action = driver.find_element_by_id("sso_submit")
    login_action.click()


if __name__ == "__main__":
    init()
    login()