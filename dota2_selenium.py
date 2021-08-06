from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import youtube_dl
import time
import os
import json
import requests
import sys


LOCAL_TEST = True
LONG_GAP = 10
SHORT_GAP = 2


target_youtube_user = [
    "NoobfromuaDota2",
    "DotadigestDD"
]


def upload():
    driver = webdriver.Chrome()

    print("start uploading")

    # options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    # options.add_argument('--no-sandbox')
    # options.add_argument("--disable-dev-shm-usage")
    # options.add_argument("--window-size=1920,3000")
    # options.add_argument("--start-maximized")
    # driver = webdriver.Chrome(options=options)

    # 初始化过程
    try:
        driver.maximize_window()
        # 创作平台主页
        print("start init")
        driver.get("https://studio.ixigua.com/welcome")

        time.sleep(LONG_GAP)
        print("init success")
    except Exception as e:
        print("init error")
        print(e)
        driver.quit()
        return False

    # 登录过程
    try:
        attempt = 1
        # 登录按钮
        while True:
            print("attempt: {}".format(attempt))
            print("login button")
            driver.find_element_by_class_name("login-btn").click()
            time.sleep(SHORT_GAP)

            # 切换为密码登录
            print("switch")
            driver.find_element_by_class_name("web-login-link-list").click()
            time.sleep(SHORT_GAP)

            # 输入账号密码
            print("username-password")
            driver.find_element_by_class_name("web-login-normal-input__input").send_keys(14701021843)
            driver.find_element_by_class_name("web-login-button-input__input").send_keys("ty1994214")
            driver.find_element_by_xpath("//*[@id='BD_Login_Form']/div/article/article/div[1]/div[1]/div[2]/article/div[5]/button").click()
            # driver.find_element_by_class_name("web-login-button").click()
            time.sleep(LONG_GAP)

            if driver.current_url == "https://studio.ixigua.com/welcome":
                driver.refresh()
                attempt += 1
            else:
                break

        print("login success")
    except Exception as e:
        print("login error")
        print(e)
        driver.quit()
        return False

    # 上传过程
    try:
        print(driver.get_window_size())
        print(len(driver.window_handles))
        for handle in driver.window_handles:
            print(handle)
        # 发布视频按钮
        print("upload button")
        driver.find_element_by_class_name("upload-btn").click()
        time.sleep(SHORT_GAP)
        # 上传视频
        print("upload video")
        if LOCAL_TEST:
            driver.find_element_by_xpath("//input[@type='file']").send_keys(r"C:\Users\Lemon_Tyd\Videos\test.mp4")
        else:
            driver.find_element_by_xpath("//input[@type='file']").send_keys(get_video())
        time.sleep(LONG_GAP)
        # 输入标题
        print("enter title")
        if LOCAL_TEST:
            driver.find_element_by_xpath("//*[@id='js-video-list-content']/div/div[2]/div[2]/div[2]/div/div/div/div/div/div/div[2]/div/div/div/div").send_keys("测试标题123")
        else:
            driver.find_element_by_xpath("//*[@id='js-video-list-content']/div/div[2]/div[2]/div[2]/div/div/div/div/div/div/div[2]/div/div/div/div").send_keys(get_title())
        time.sleep(SHORT_GAP)
        # 上传封面按钮
        print("thumbnail button")
        driver.find_element_by_class_name("m-xigua-upload").click()
        time.sleep(SHORT_GAP)
        # 选择本地上传
        print("choose local file")
        driver.find_element_by_xpath("/html/body/div[4]/div/div[2]/div/div[1]/ul/li[2]").click()
        time.sleep(SHORT_GAP)
        # 上传图片
        print("upload thumbnail")
        if LOCAL_TEST:
            driver.find_element_by_xpath("//input[@type='file']").send_keys(r"C:\Users\Lemon_Tyd\Videos\test.jpg")
        else:
            driver.find_element_by_xpath("//input[@type='file']").send_keys(get_thumbnail())
        time.sleep(LONG_GAP)
        # 点击确认
        print("confirm thumbnail")
        driver.find_element_by_xpath("//*[@id='tc-ie-base-content']/div[2]/div[2]/div[3]/div[3]/button[2]").click()
        time.sleep(SHORT_GAP)
        # 点击确认
        print("double confirm thumbnail")
        driver.find_element_by_xpath("/html/body/div[5]/div/div[2]/div/div[2]/button[2]").click()
        time.sleep(SHORT_GAP)
        # 选择视频类型为转载
        print("reproduce")
        driver.find_element_by_xpath("//*[@id='js-video-list-content']/div/div[2]/div[6]/div[2]/div/div/label[2]").click()
        time.sleep(SHORT_GAP)
        # 展开更多选项
        print("more options")
        driver.find_element_by_xpath("//*[@id='js-video-list-content']/div/div[2]/div[8]/div").click()
        time.sleep(SHORT_GAP)
        # 向下滚动滚动条
        print("scroll down")
        driver.execute_script("window.scrollBy(0,1000)")
        time.sleep(SHORT_GAP)
        # 输入简介
        print("description")
        driver.find_element_by_xpath("//*[@id='js-video-list-content']/div/div[2]/div[8]/div[2]/div[2]/div/div/div/div/div/div[2]/div/div/div/div").send_keys("DOTA2精彩视频集锦")
        time.sleep(SHORT_GAP)
        # 互动贴纸按钮
        print("paster")
        driver.find_element_by_class_name("video-sticker-btn-main").click()
        time.sleep(SHORT_GAP)
        # 点击点赞引导
        print("thumb up")
        driver.find_element_by_xpath("/html/body/div[5]/div[2]/div/div[3]/div[2]/div/div[1]/div[2]/div[2]").click()
        time.sleep(SHORT_GAP)
        # 输入起始时间，分+秒
        print("start-end time")
        if LOCAL_TEST:
            driver.find_element_by_xpath("//*[@id='StartTime']/div/div[1]/span/span/input").send_keys(0)
            driver.find_element_by_xpath("//*[@id='StartTime']/div/div[2]/span/span/input").send_keys(1)
        else:
            driver.find_element_by_xpath("//*[@id='StartTime']/div/div[1]/span/span/input").send_keys(1)
            driver.find_element_by_xpath("//*[@id='StartTime']/div/div[2]/span/span/input").send_keys(0)
        time.sleep(SHORT_GAP)
        # 输入持续时间
        print("last time")
        if LOCAL_TEST:
            driver.find_element_by_xpath("//*[@id='Duration']/div/div/span/span/input").send_keys(Keys.CONTROL + 'a')
            driver.find_element_by_xpath("//*[@id='Duration']/div/div/span/span/input").send_keys(1)
        else:
            driver.find_element_by_xpath("//*[@id='Duration']/div/div/span/span/input").send_keys(Keys.CONTROL + 'a')
            driver.find_element_by_xpath("//*[@id='Duration']/div/div/span/span/input").send_keys(10)
        time.sleep(SHORT_GAP)
        # 点击确认
        print("confirm paster")
        driver.find_element_by_xpath("/html/body/div[5]/div[2]/div/div[3]/div[2]/div/div[3]/div[2]/div/div[2]").click()
        time.sleep(SHORT_GAP)

        # 上传字幕
        print("subtitle")
        driver.find_element_by_class_name("form-item-add-caption__empty").click()
        time.sleep(SHORT_GAP)
        if LOCAL_TEST:
            driver.find_element_by_xpath("/html/body/div[5]/div[2]/div/div[3]/div[1]/div[3]/div[1]/div[2]/div/input").send_keys(r"C:\Users\Lemon_Tyd\Videos\T1 vs SMG - SEA GROUP STAGE - BTS PRO SERIES 7 DOTA 2-mfc7QPBberc.zh-Hans.srt")
            time.sleep(LONG_GAP)
            driver.find_element_by_class_name("add-caption-modal__button").click()
            time.sleep(SHORT_GAP)
            driver.find_element_by_xpath("/html/body/div[5]/div[2]/div/div[3]/div[1]/div[3]/div[2]/div[2]/div/input").send_keys(r"C:\Users\Lemon_Tyd\Videos\T1 vs SMG - SEA GROUP STAGE - BTS PRO SERIES 7 DOTA 2-mfc7QPBberc.en.srt")
            time.sleep(LONG_GAP)
        else:
            driver.find_element_by_xpath("/html/body/div[5]/div[2]/div/div[3]/div[1]/div[3]/div[2]/div[2]/div/input").send_keys(get_en_sub())
            time.sleep(LONG_GAP)
            driver.find_element_by_class_name("add-caption-modal__button").click()
            time.sleep(SHORT_GAP)
            driver.find_element_by_xpath("/html/body/div[5]/div[2]/div/div[3]/div[1]/div[3]/div[1]/div[2]/div/input").send_keys(get_zh_sub())
            time.sleep(LONG_GAP)
        # 确认上传字幕
        print("confirm subtitle")
        driver.find_element_by_class_name("byte-btn-primary").click()
        time.sleep(SHORT_GAP)

        # # 取消勾选抖音内容同步（不知道为啥现在不是默认勾选，先注释掉了）
        # driver.find_element_by_xpath("//*[@id='js-video-list-content']/div/div[2]/div[8]/div[8]/div[2]/div/label/input").send_keys(False)
        # # driver.find_element_by_xpath("//*[@id='js-video-list-content']/div/div[2]/div[8]/div[8]/div[2]/div/label/span/div").click()
        # time.sleep(1)

        # 点击确认上传
        driver.find_element_by_xpath("//*[@id='js-submit-0']/button").click()
        time.sleep(SHORT_GAP)
        print("upload success")
    except Exception as e:
        print("upload error")
        print(e)
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
        if file.endswith(".jpg"):
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
        print(e)
        return 0
    return 1


def vtt2srt():
    try:
        for file in os.listdir(os.getcwd()):
            if file.endswith(".vtt"):
                file_path = os.getcwd() + "/" + file
                file_name = file[0:-4]
                print("Processing with file:    " + file_path)
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
        print("vtt to srt error")
        return False
    print("vtt 2 srt success")
    return True
    # try:
    #     for file in os.listdir(os.getcwd()):
    #         if not (file.endswith(".py") or file.endswith(".txt")):
    #             # print(os.getcwd() + "\\" + file)
    #             os.remove(os.getcwd() + "\\" + file)
    # except:
    #     print("delete error")
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
        return -1


def check_uploaded(video_id):
    history = open("history.txt", "a+")
    history.seek(0)
    lines = history.readlines()
    history.close()
    if (video_id + '\n') in lines:
        return True
    return False


def check_download_complete():
    video_flag = False
    thumbnail_flag = False
    en_subtitle_flag = False
    zh_subtitle_flag = False
    info_flag = False
    for file in os.listdir(os.getcwd()):
        if file.endswith(".mp4"):
            video_flag = True
            print("mp4: " + file)
        elif file.endswith(".jpg"):
            thumbnail_flag = True
            print("jpg: " + file)
        elif file.endswith(".en.srt"):
            en_subtitle_flag = True
            print("en.srt: " + file)
        elif file.endswith(".zh-Hans.srt"):
            zh_subtitle_flag = True
            print("zh.srt: " + file)
        elif file.endswith(".info.json"):
            info_flag = True
            print("json: " + file)
    # video_flag = True
    return (video_flag and thumbnail_flag and en_subtitle_flag and zh_subtitle_flag and info_flag)


# 下载流程
def download_procedure(video_id):
    video_url = "https://www.youtube.com/watch?v={}".format(video_id)
    download_result = download(video_url)
    if download_result is False:
        print("download error")
        return False
    vtt2srt_result = vtt2srt()
    if vtt2srt_result is False:
        print("vtt 2 srt error")
        return False
    download_complete_result = check_download_complete()
    if not download_complete_result:
        print("download incomplete, something is missing")
        return False
    return True


# 上传流程
def upload_procedure():
    upload_success = upload()
    return upload_success


# 清理流程
def delete_procedure():
    try:
        for file in os.listdir(os.getcwd()):
            if not (file.endswith(".py") or file.endswith(".txt") or file == "chromedriver"):
                # print(os.getcwd() + "\\" + file)
                os.remove(os.getcwd() + "/" + file)
    except:
        print("delete error")
        return False
    return True


# 通知流程
def notify_procedure(result):
    pass


if __name__ == "__main__":

    if LOCAL_TEST:
        upload()

    # while True:
    #     for username in target_youtube_user:
    #         video_list = find_all(username)
    #         for video_id in video_list:
    #             if not check_uploaded(video_id):
    #                 download_success = download_procedure(video_id)
    #                 if not download_success:
    #                     notify_procedure("download fail")
    #                     delete_procedure()
    #                     break
    #                 upload_success = upload_procedure()
    #                 if not upload_success:
    #                     notify_procedure("upload fail")
    #                     delete_procedure()
    #                     break
    #                 history = open("history.txt", "a+")
    #                 history.write(video_id + "\n")
    #                 history.close()
    #                 delete_success = delete_procedure()
    #                 if not delete_success:
    #                     notify_procedure("delete fail")
    #                     break
    #                 notify_procedure("download and upload success")

###############################################################################
    else:
        username = "NoobfromuaDota2"
        video_list = find_all(username)
        if video_list == -1:
            print("get video list fail")
            sys.exit(1)
        video_id = video_list[1]
        if not check_uploaded(video_id):
            download_success = download_procedure(video_id)
            if not download_success:
                notify_procedure("download fail")
                print("download fail")
                delete_procedure()
                sys.exit(1)
            upload_success = upload_procedure()
            if not upload_success:
                notify_procedure("upload fail")
                print("upload fail")
                delete_procedure()
                sys.exit(1)
            history = open("history.txt", "a+")
            history.write(video_id + "\n")
            history.close()
            delete_success = delete_procedure()
            if not delete_success:
                notify_procedure("delete fail")
                print("delete fail")
                sys.exit(1)
            notify_procedure("download and upload success")
            sys.exit(0)
