from selenium import webdriver
import time
import json


# options = webdriver.ChromeOptions()
# options.add_argument('--headless')
# options.add_argument('window-size=1920x3000')
# driver = webdriver.Chrome(options=options)

driver = webdriver.Chrome()


def init():
    driver.maximize_window()
    driver.get("https://www.ixigua.com/")

    time.sleep(5)


def login():
    login_btn = driver.find_element_by_class_name("loginButton")
    login_btn.click()

    time.sleep(10)

    switch = driver.find_element_by_id("sso_pwd_login")
    switch.click()

    time.sleep(1)

    username = driver.find_element_by_name("username").send_keys(14701021843)
    pwd = driver.find_element_by_name("password").send_keys("ty1994214")
    login_action = driver.find_element_by_id("sso_submit")
    login_action.click()

    time.sleep(1)


def upload():
    driver.get("https://studio.ixigua.com/upload")

    time.sleep(3)


def test():
    time.sleep(3)
    print(driver.get_window_size())
    # head_img = driver.find_element_by_class_name("BU-Component-Header-Avatar__image")
    # print(head_img)
    # time.sleep(1)
    # driver.save_screenshot("screenshot.png")


if __name__ == "__main__":
    init()
    login()
    upload()
