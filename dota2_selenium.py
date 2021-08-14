from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import youtube_dl
import time
import os
import json
import requests
import sys
import logging
import smtplib
from email.mime.text import MIMEText
from email.header import Header

LOCAL_TEST = False

# 第三方 SMTP 服务
mail_host = "smtp.163.com"  # 设置服务器
mail_user = "dota2daily"  # 用户名
mail_pass = "IMXEZHFKBGMLNFCW"  # 口令

sender = 'dota2daily@163.com'
receivers = ['931770556@qq.com', '525370782@qq.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

if LOCAL_TEST:
    LONG_GAP = 20
    SHORT_GAP = 5
    TRY_GAP = 0.5
else:
    LONG_GAP = 120
    SHORT_GAP = 20
    TRY_GAP = 1


target_youtube_user = [
    "NoobfromuaDota2",
    "DotadigestDD"
]

no_sub_flag = False

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
logging.basicConfig(filename="log.log", level=logging.INFO, format=LOG_FORMAT, datefmt=DATE_FORMAT)


def upload():
    if LOCAL_TEST:
        driver = webdriver.Chrome()
        driver.maximize_window()
        desired_capabilities = DesiredCapabilities.CHROME
        desired_capabilities["pageLoadStrategy"] = "none"
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
    else:
        desired_capabilities = DesiredCapabilities.CHROME
        desired_capabilities["pageLoadStrategy"] = "none"
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,3000")
        options.add_argument("--start-maximized")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-default-apps")
        options.add_argument("--disable-sync")
        options.add_argument("--disable-translate")
        driver = webdriver.Chrome(options=options)

    # 开始上传过程
    logging.info("start uploading")
    time.sleep(SHORT_GAP)
    try:
        # 创作平台主页
        logging.info("open homepage")
        driver.get("https://studio.ixigua.com")
        time.sleep(SHORT_GAP)
        logging.info("init success")

        # 清除旧的cookie
        logging.info("clear cookies")
        driver.delete_all_cookies()

        # 读取cookie
        logging.info("read cookies")
        with open('cookies.txt', 'r') as f:
            # 使用json读取cookies 注意读取的是文件 所以用load而不是loads
            cookies_list = json.load(f)
            for cookie in cookies_list:
                cookie['expiry'] = 2000000000
                driver.add_cookie(cookie)

        # 重定向，完成登录
        logging.info("redirect")
        driver.get("https://studio.ixigua.com/?is_new_connect=0&is_new_user=0")
        time.sleep(SHORT_GAP)
        if driver.current_url == "https://studio.ixigua.com/?is_new_connect=0&is_new_user=0":
            logging.info("cookie login success")
        else:
            logging.error("cookie login fail")
            notify_procedure("cookie登录失败，请手动更新cookie")
            driver.quit()
            return False

        # 发布视频按钮
        logging.info("upload button")
        WebDriverWait(driver, LONG_GAP, TRY_GAP).until(EC.element_to_be_clickable((By.CLASS_NAME, "upload-btn"))).click()

        # 上传视频
        video_input = WebDriverWait(driver, LONG_GAP, TRY_GAP).until(EC.presence_of_element_located((By.XPATH, "//input[@type='file']")))
        logging.info("upload video")
        if LOCAL_TEST:
            video_input.send_keys(r"C:\Users\Lemon_Tyd\Videos\test.mp4")
        else:
            video_input.send_keys(get_video())

        # 输入标题
        logging.info("enter title")
        title_input = WebDriverWait(driver, LONG_GAP, TRY_GAP).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='js-video-list-content']/div/div[2]/div[2]/div[2]/div/div/div/div/div/div/div[2]/div/div/div/div")))
        if LOCAL_TEST:
            title_input.send_keys("测试标题123")
        else:
            title_input.send_keys(rename(get_title()))

        # 上传封面按钮
        logging.info("thumbnail button")
        WebDriverWait(driver, LONG_GAP, TRY_GAP).until(EC.element_to_be_clickable((By.CLASS_NAME, "m-xigua-upload"))).click()

        # 选择本地上传
        logging.info("choose local file")
        WebDriverWait(driver, LONG_GAP, TRY_GAP).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[4]/div/div[2]/div/div[1]/ul/li[2]"))).click()

        # 上传图片
        logging.info("upload thumbnail")
        video_input = WebDriverWait(driver, LONG_GAP, TRY_GAP).until(EC.presence_of_element_located((By.XPATH, "//input[@type='file']")))
        if LOCAL_TEST:
            video_input.send_keys(r"C:\Users\Lemon_Tyd\Videos\test.jpg")
        else:
            video_input.send_keys(get_thumbnail())

        # 这里的确认按钮有一个opacity从0.4变为1的动画效果，实际是不可点击的，所以手动sleep一下
        time.sleep(SHORT_GAP)

        # 点击确认
        logging.info("confirm thumbnail")
        WebDriverWait(driver, LONG_GAP, TRY_GAP).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='tc-ie-base-content']/div[2]/div[2]/div[3]/div[3]/button[2]"))).click()

        # 双重确认
        logging.info("double confirm thumbnail")
        WebDriverWait(driver, LONG_GAP, TRY_GAP).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[5]/div/div[2]/div/div[2]/button[2]"))).click()

        # 确认上传封面后需要一点时间让界面消失、更新
        time.sleep(SHORT_GAP)

        # 选择视频类型为转载
        logging.info("reproduce")
        WebDriverWait(driver, LONG_GAP, TRY_GAP).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='js-video-list-content']/div/div[2]/div[6]/div[2]/div/div/label[2]/span/div"))).click()

        # 展开更多选项
        logging.info("more options")
        WebDriverWait(driver, LONG_GAP, TRY_GAP).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='js-video-list-content']/div/div[2]/div[8]/div"))).click()

        # 向下滚动滚动条
        logging.info("scroll down")
        driver.execute_script("window.scrollBy(0,1000)")

        # 输入简介
        logging.info("description")
        WebDriverWait(driver, LONG_GAP, TRY_GAP).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='js-video-list-content']/div/div[2]/div[8]/div[2]/div[2]/div/div/div/div/div/div[2]/div/div/div/div"))).send_keys("DOTA2精彩视频" + "\n" + get_title())

        # 互动贴纸按钮
        logging.info("paster")
        WebDriverWait(driver, LONG_GAP, TRY_GAP).until(EC.element_to_be_clickable((By.CLASS_NAME, "video-sticker-btn-main"))).click()

        # 点击点赞引导
        logging.info("thumb up")
        WebDriverWait(driver, LONG_GAP, TRY_GAP).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[5]/div[2]/div/div[3]/div[2]/div/div[1]/div[2]/div[2]"))).click()

        # 输入起始时间，分+秒
        logging.info("start-end time")
        start_min = WebDriverWait(driver, LONG_GAP, TRY_GAP).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='StartTime']/div/div[1]/span/span/input")))
        start_sec = WebDriverWait(driver, LONG_GAP, TRY_GAP).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='StartTime']/div/div[2]/span/span/input")))
        if LOCAL_TEST:
            start_min.send_keys(0)
            start_sec.send_keys(1)
        else:
            start_min.send_keys(1)
            start_sec.send_keys(0)

        # 输入持续时间
        logging.info("last time")
        last_time = WebDriverWait(driver, LONG_GAP, TRY_GAP).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='Duration']/div/div/span/span/input")))
        if LOCAL_TEST:
            last_time.send_keys(Keys.CONTROL + 'a')
            last_time.send_keys(1)
        else:
            last_time.send_keys(Keys.CONTROL + 'a')
            last_time.send_keys(10)

        # 点击确认
        logging.info("confirm paster")
        WebDriverWait(driver, LONG_GAP, TRY_GAP).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[5]/div[2]/div/div[3]/div[2]/div/div[3]/div[2]/div/div[2]"))).click()

        # 确认贴纸后需要一点时间让界面消失、刷新
        time.sleep(SHORT_GAP)

        global no_sub_flag
        if no_sub_flag is False:
            # 添加字幕
            logging.info("subtitle")
            WebDriverWait(driver, LONG_GAP, TRY_GAP).until(EC.element_to_be_clickable((By.CLASS_NAME, "form-item-add-caption__empty"))).click()

            # 中文字幕
            logging.info("zh-subtitle")
            zh_sub = WebDriverWait(driver, LONG_GAP, TRY_GAP).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[5]/div[2]/div/div[3]/div[1]/div[3]/div[1]/div[2]/div/input")))
            if LOCAL_TEST:
                zh_sub.send_keys(r"C:\Users\Lemon_Tyd\Videos\T1 vs SMG - SEA GROUP STAGE - BTS PRO SERIES 7 DOTA 2-mfc7QPBberc.zh-Hans.srt")
            else:
                zh_sub.send_keys(get_zh_sub())

            # 添加第二个字幕
            logging.info("add 2nd subtitle")
            WebDriverWait(driver, LONG_GAP, TRY_GAP).until(EC.element_to_be_clickable((By.CLASS_NAME, "add-caption-modal__button"))).click()

            # 英文字幕
            logging.info("en-subtitle")
            en_sub = WebDriverWait(driver, LONG_GAP, TRY_GAP).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[5]/div[2]/div/div[3]/div[1]/div[3]/div[2]/div[2]/div/input")))
            if LOCAL_TEST:
                en_sub.send_keys(r"C:\Users\Lemon_Tyd\Videos\T1 vs SMG - SEA GROUP STAGE - BTS PRO SERIES 7 DOTA 2-mfc7QPBberc.en.srt")
            else:
                en_sub.send_keys(get_en_sub())

            # 确认上传字幕
            logging.info("confirm subtitle")
            WebDriverWait(driver, LONG_GAP, TRY_GAP).until(EC.element_to_be_clickable((By.CLASS_NAME, "byte-btn-primary"))).click()

        # 确认视频上传完毕
        WebDriverWait(driver, LONG_GAP * 10, TRY_GAP).until(EC.visibility_of_element_located((By.CLASS_NAME, "status")))
        logging.info("video upload finish")

        # 点击确认上传
        WebDriverWait(driver, LONG_GAP, TRY_GAP).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='js-submit-0']/button"))).click()
        logging.info("upload success")
    except Exception as e:
        logging.error("upload error")
        logging.error(e)
        driver.quit()
        return False
    driver.quit()
    return True


def get_title():
    for file in os.listdir(os.getcwd()):
        if file.endswith(".info.json"):
            with open((os.getcwd() + '/' + file), "r") as f:
                info = json.load(f)
            return info['title']


def get_video():
    for file in os.listdir(os.getcwd()):
        if file.endswith(".mp4"):
            video_path = os.getcwd() + '/' + file
            return video_path


def get_thumbnail():
    for file in os.listdir(os.getcwd()):
        if file.endswith(".jpg") or file.endswith(".webp"):
            thumbnail_path = os.getcwd() + '/' + file
            return thumbnail_path


def get_en_sub():
    for file in os.listdir(os.getcwd()):
        if file.endswith(".en.srt"):
            en_sub_path = os.getcwd() + '/' + file
            return en_sub_path


def get_zh_sub():
    for file in os.listdir(os.getcwd()):
        if file.endswith(".zh-Hans.srt"):
            zh_sub_path = os.getcwd() + '/' + file
            return zh_sub_path


def download(youtube_url):
    try:
        ydl_opts = {
            # 保存最佳封面
            'writethumbnail': True,
            # 最佳视频+最佳音频（ffmpeg自动合并）
            'format': "bestvideo+bestaudio",
            # 第三方下载工具
            'external_downloader': "aria2c",
            # 第三方下载工具参数，16线程，指定块大小1M
            'external_downloader_args': ["-x16", "-k1M"],
            # 视频信息json文件，用于获取id和title等
            'writeinfojson': True,
            # 保存自动字幕
            'writeautomaticsub': True,
            # 选择字幕格式
            'subtitlesformat': 'best/srt',
            # 中英字幕
            'subtitleslangs': ['en', 'zh-Hans'],
            # # 是否下载视频文件（测试用）
            # 'skip_download': True
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_url])
    except Exception as e:
        logging.info(e)
        return 0
    return 1


def vtt2srt():
    try:
        sub_exist_flag = False
        for file in os.listdir(os.getcwd()):
            if file.endswith(".vtt"):
                sub_exist_flag = True
                file_path = os.getcwd() + "/" + file
                file_name = file[0:-4]
                logging.info("Processing with file:    " + file_path)
                with open(file_path, "r", encoding="utf-8") as fin:
                    file_content = fin.readlines()
                    line_num = 2
                    file_max_line_num = len(file_content)
                    with open(file_name + ".srt", "w", encoding="gbk") as fout:
                        fout.write("1\n")
                        for i in range(2, file_max_line_num):
                            fout.write(file_content[i].replace(".", ","))
                            if file_content[i].strip() == "" and i+1 < file_max_line_num and file_content[i+1].strip() != "":
                                fout.write(str(line_num) + "\n")
                                line_num += 1
    except:
        logging.info("vtt to srt error")
        return False
    if not sub_exist_flag:
        logging.info("no subtitles")
    return True
    # try:
    #     for file in os.listdir(os.getcwd()):
    #         if not (file.endswith(".py") or file.endswith(".txt")):
    #             # logging.info(os.getcwd() + "\\" + file)
    #             os.remove(os.getcwd() + "\\" + file)
    # except:
    #     logging.info("delete error")
    #     return False
    # return True


def find_all(username):
    id_list = []
    sub = "watch?v="
    s = requests.get("https://www.youtube.com/c/{}/videos".format(username)).text
    index = s.find(sub)
    while index != -1:
        video_id = s[(index + 8): (index + 19)]
        id_list.append(video_id)
        index = s.find(sub, index + 1)

    if len(id_list) > 0:
        return id_list
    else:
        logging.error("get video list for '{}' fail".format(username))
        notify_procedure("获取youtube账户：'{}' 视频列表信息失败，请检查！".format(username))
        sys.exit(1)


def check_uploaded(video_id):
    upload_history = open("history.txt", "a+")
    upload_history.seek(0)
    lines = upload_history.readlines()
    upload_history.close()
    if (video_id + '\n') in lines:
        return True
    return False


def check_download_complete():
    video_flag = False
    thumbnail_flag = False
    en_subtitle_flag = False
    zh_subtitle_flag = False
    info_flag = False
    global no_sub_flag
    for file in os.listdir(os.getcwd()):
        if file.endswith(".mp4"):
            video_flag = True
            logging.info("video: " + file)
        elif file.endswith(".jpg") or file.endswith(".webp"):
            thumbnail_flag = True
            logging.info("thumbnail: " + file)
        elif file.endswith(".en.srt"):
            en_subtitle_flag = True
            logging.info("en-srt: " + file)
        elif file.endswith(".zh-Hans.srt"):
            zh_subtitle_flag = True
            logging.info("zh-srt: " + file)
        elif file.endswith(".info.json"):
            info_flag = True
            logging.info("json: " + file)
    if en_subtitle_flag is False or zh_subtitle_flag is False:
        no_sub_flag = True
    return (video_flag and thumbnail_flag and info_flag)


def rename(video_title):
    name_result = ""
    video_title_split = video_title.split(" ")
    for word in video_title_split:
        if len(name_result + word + " ") <= 30:
            name_result += word + " "
        else:
            break
    return name_result


# 下载流程
def download_procedure(video_id):
    global no_sub_flag
    no_sub_flag = False
    video_url = "https://www.youtube.com/watch?v={}".format(video_id)
    logging.info("start download {}".format(video_id))
    download_result = download(video_url)
    if download_result is False:
        logging.error("download error")
        return False
    logging.info("download success {}".format(video_id))
    logging.info("start vtt2srt {}".format(video_id))
    vtt2srt_result = vtt2srt()
    if vtt2srt_result is False:
        logging.error("vtt 2 srt error")
        return False
    logging.info("vtt2srt success {}".format(video_id))
    logging.info("start check download complete {}".format(video_id))
    download_complete_result = check_download_complete()
    if not download_complete_result:
        logging.error("download incomplete, something is missing")
        return False
    logging.info("check download success {}".format(video_id))
    return True


# 上传流程
def upload_procedure():
    upload_attempt = 1
    while True:
        if upload_attempt > 5:
            notify_procedure("upload fail after 3 attempts")
            return False
        upload_result = upload()
        if upload_result:
            return True
        else:
            upload_attempt += 1
            time.sleep(LONG_GAP)


# 清理流程
def delete_procedure():
    for file in os.listdir(os.getcwd()):
        if not (file.endswith(".py") or file.endswith(".txt") or file.endswith(".log") or file == "chromedriver"):
            os.remove(os.getcwd() + "/" + file)
    logging.info("delete finish")


# 通知流程
def notify_procedure(result):
    for receiver in receivers:
        message = MIMEText(result, 'plain', 'utf-8')
        message['From'] = sender
        message['To'] = receiver

        subject = 'dota2daily - 上传结果通知'
        message['Subject'] = Header(subject, 'utf-8')

        try:
            smtpObj = smtplib.SMTP()
            smtpObj.connect(mail_host, 25)  # 25 为 SMTP 端口号
            smtpObj.login(mail_user, mail_pass)
            smtpObj.sendmail(sender, receiver, message.as_string())
            logging.info("邮件发送成功")
            smtpObj.quit()
        except smtplib.SMTPException as e:
            logging.error("Error: 无法发送邮件", e)
            return False
    return True


if __name__ == "__main__":

    # if LOCAL_TEST:
    #     upload()
    logging.info("job start")
    while True:
        for username in target_youtube_user:
            video_list = find_all(username)
            for video_id in video_list:
                if not check_uploaded(video_id):
                    start_time = time.time()
                    download_success = download_procedure(video_id)
                    if not download_success:
                        logging.error("download fail {}".format(video_id))
                        notify_procedure("下载youtube账户：'{}'\n\n视频：'{}'\n\n失败\n\nid为：{}\n\n请检查！".format(username, get_title(), video_id))
                        delete_procedure()
                        sys.exit(1)
                    upload_success = upload_procedure()
                    if not upload_success:
                        logging.error("upload fail {}".format(video_id))
                        notify_procedure("上传youtube账户：'{}'\n\n视频：'{}'\n\n失败\n\nid为：{}\n\n请检查！".format(username, get_title(), video_id))
                        delete_procedure()
                        sys.exit(1)
                    history = open("history.txt", "a+")
                    history.write(str(video_id) + "\n")
                    history.close()
                    end_time = time.time()
                    notify_procedure("下载并上传youtube账户：'{}'\n\n视频：'{}'\n\n成功\n\nid为：{}\n\n共耗时 {}秒".format(username, get_title(), video_id, end_time - start_time))
                    delete_procedure()
            time.sleep(LONG_GAP)
