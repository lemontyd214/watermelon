from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time


def generate():
    # desired_capabilities = DesiredCapabilities.CHROME
    # desired_capabilities["pageLoadStrategy"] = "none"
    # options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    # options.add_argument('--no-sandbox')
    # options.add_argument("--disable-dev-shm-usage")
    # options.add_argument("--window-size=1920,3000")
    # options.add_argument("--start-maximized")
    # options.add_argument("--disable-extensions")
    # options.add_argument("--disable-gpu")
    # options.add_argument("--disable-default-apps")
    # options.add_argument("--disable-sync")
    # options.add_argument("--disable-translate")
    # driver = webdriver.Chrome(options=options)

    driver = webdriver.Chrome()
    driver.maximize_window()
    desired_capabilities = DesiredCapabilities.CHROME
    desired_capabilities["pageLoadStrategy"] = "none"

    try:
        driver.get("https://studio.ixigua.com")
        time.sleep(60)
        cookies = driver.get_cookies()
        jsonCookies = json.dumps(cookies)
        with open('xigua_cookies.txt', 'w') as f:
            f.write(jsonCookies)
        print("cookie更新完成")
        driver.quit()
    except Exception as e:
        print("error")
        print(e)
        driver.quit()


if __name__ == "__main__":
    generate()
