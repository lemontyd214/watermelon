from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import json


def login():
    driver = webdriver.Chrome()
    driver.maximize_window()
    desired_capabilities = DesiredCapabilities.CHROME
    desired_capabilities["pageLoadStrategy"] = "none"


    try:
        driver.get("https://studio.ixigua.com")

        driver.delete_all_cookies()

        with open('xigua_cookies.json', 'r') as f:
            cookies_list = json.load(f)
            for cookie in cookies_list:
                cookie['expiry'] = 2000000000
                driver.add_cookie(cookie)

        driver.get("https://studio.ixigua.com/?is_new_connect=0&is_new_user=0")
        time.sleep(10)
    except Exception as e:
        print(e)
        driver.quit()
        return False
    driver.quit()
    return True

if __name__ == "__main__":
    login()