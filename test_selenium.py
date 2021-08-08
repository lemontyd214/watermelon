from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import youtube_dl
import time
import os
import json
import requests
import sys


LONG_GAP = 20
SHORT_GAP = 5


def upload():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,3000")
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    print("start uploading")
    # driver = webdriver.Chrome()
    # driver.maximize_window()
    # 初始化过程
    # try:
        # 创作平台主页
    print("start init")

    driver.get("https://studio.ixigua.com")

    time.sleep(LONG_GAP)
    driver.delete_all_cookies()
    time.sleep(SHORT_GAP)
    with open('cookies.txt', 'r') as f:
        # 使用json读取cookies 注意读取的是文件 所以用load而不是loads
        cookies_list = json.load(f)
        for cookie in cookies_list:
            cookie['expiry'] = 2000000000
            driver.add_cookie(cookie)
    print(driver.current_url)
    print("init success")

    print("goto")
    driver.get("https://studio.ixigua.com/?is_new_connect=0&is_new_user=0")
    print(driver.current_url)
    # driver.quit()
    # except Exception as e:
    #     print("init error")
    #     # print('time out after 10 second when loading page!!!')
    #     print(e)
    #     # driver.execute_script("window.stop()")
    #     # print(driver.page_source)
    #     return False

    # # 登录过程
    # # try:
    # # attempt = 1
    # # 登录按钮
    # # while True:
    # # print("attempt: {}".format(attempt))
    # print("login button")
    # driver.find_element_by_class_name("login-btn").click()
    # time.sleep(SHORT_GAP)
    #
    # # # 切换为密码登录
    # # print("switch")
    # # driver.find_element_by_class_name("web-login-link-list").click()
    # # time.sleep(SHORT_GAP)
    # #
    # # # 输入账号密码
    # # print("username-password")
    # # driver.find_element_by_class_name("web-login-normal-input__input").send_keys(14701021843)
    # # driver.find_element_by_class_name("web-login-button-input__input").send_keys("ty1994214")
    # # # driver.find_element_by_xpath("//*[@id='BD_Login_Form']/div/article/article/div[1]/div[1]/div[2]/article/div[5]/button").click()
    # # driver.find_element_by_class_name("web-login-button").send_keys(Keys.ENTER)
    # # time.sleep(LONG_GAP)
    #
    # # linux第一次用验证码登录
    # print("enter tel")
    # driver.find_element_by_class_name("web-login-normal-input__input").send_keys(14701021843)
    # # print("send code")
    # # driver.find_element_by_xpath("//*[@id='BD_Login_Form']/div/article/article/div[1]/div[1]/div[2]/article/div[2]/div/span").send_keys(Keys.ENTER)
    # # print("code sent")
    # code = input("请输入验证码： ")
    # time.sleep(LONG_GAP)
    # print("enter code")
    # driver.find_element_by_class_name("web-login-button-input__input").send_keys(code)
    # print("click login")
    # driver.find_element_by_class_name("web-login-button").send_keys(Keys.ENTER)
    # time.sleep(LONG_GAP)
    #
    # print("current url: {}".format(driver.current_url))
    # if driver.current_url == "https://studio.ixigua.com/welcome":
    #     print(driver.find_element_by_class_name("web-login-error").get_attribute("innerHTML"))
    # else:
    #     with open('cookies.txt', 'w') as f:
    #         # 将cookies保存为json格式
    #         f.write(json.dumps(driver.get_cookies()))
    #
    # # if driver.current_url == "https://studio.ixigua.com/welcome":
    # #     driver.refresh()
    #     # attempt += 1
    # # else:
    # #     break
    time.sleep(LONG_GAP)

    print("login success")
    driver.quit()
    # except Exception as e:
    #     print("login error")
    #     print(e)
    #     driver.quit()
    #     return False


def cookie_upload():
    desired_capabilities = DesiredCapabilities.CHROME
    desired_capabilities["pageLoadStrategy"] = "none"
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,3000")
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)

    print("start uploading")

    # 初始化过程
    try:
        # 创作平台主页
        print("start init")
        driver.get("https://studio.ixigua.com")

        time.sleep(LONG_GAP)
        print("init success")
    except Exception as e:
        print("init error")
        print(e)
        driver.quit()
        return False

    # 登录过程
    try:
        driver.delete_all_cookies()
        time.sleep(SHORT_GAP)
        # 读取cookie
        print("read cookies")
        with open('cookies.txt', 'r') as f:
            # 使用json读取cookies 注意读取的是文件 所以用load而不是loads
            cookies_list = json.load(f)
            for cookie in cookies_list:
                cookie['expiry'] = 2000000000
                driver.add_cookie(cookie)
        time.sleep(SHORT_GAP)
        print("redirect")
        driver.get("https://studio.ixigua.com/?is_new_connect=0&is_new_user=0")
        time.sleep(SHORT_GAP)
        if driver.current_url == "https://studio.ixigua.com/?is_new_connect=0&is_new_user=0":
            print("cookie login success")
        else:
            print("cookie login fail")
            print(driver.current_url)
            return False
    except Exception as e:
        print("login error")
        print(e)
        driver.quit()
        return False


def test_double_comfirm():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("https://studio.ixigua.com")
    time.sleep(1000)


if __name__ == "__main__":
    # cookie_upload()
    # upload()
    test_double_comfirm()
