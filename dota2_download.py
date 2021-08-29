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


target_youtube_user = [
    "NoobfromuaDota2",
    "DotadigestDD"
]

if LOCAL_TEST:
    LONG_GAP = 20
    SHORT_GAP = 5
    TRY_GAP = 0.5
else:
    LONG_GAP = 120
    SHORT_GAP = 20
    TRY_GAP = 1

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
logging.basicConfig(filename="download.log", level=logging.INFO, format=LOG_FORMAT, datefmt=DATE_FORMAT)


# 下载视频+封面
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
            'writeinfojson': True
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_url])
    except Exception as e:
        logging.info(e)
        return False
    return True


'''
# 将vtt字幕文件转化为srt字幕文件
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
'''


# 获取某个youtube用户的全部视频列表
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


# 检查某个视频id是否已经上传过并记录在history.txt中
def check_uploaded(video_id):
    upload_history = open("history.txt", "a+")
    upload_history.seek(0)
    lines = upload_history.readlines()
    upload_history.close()
    if (video_id + '\n') in lines:
        return True
    return False


# 检查下载是否完整，包含视频+封面图片+json文件
def check_download_complete():
    video_flag = False
    thumbnail_flag = False
    info_flag = False
    for file in os.listdir(os.getcwd()):
        if file.endswith(".mp4") or file.endswith(".mkv"):
            video_flag = True
            logging.info("video: " + file)
        elif file.endswith(".jpg") or file.endswith(".webp"):
            thumbnail_flag = True
            logging.info("thumbnail: " + file)
        elif file.endswith(".info.json"):
            info_flag = True
            logging.info("json: " + file)
    return (video_flag and thumbnail_flag and info_flag)


# 将已下载、待上传视频id写入文件
def write_tmp(video_id, username):
    tmp = open("tmp.txt", "w")
    tmp.write(str(video_id) + "\n")
    tmp.write(username)
    tmp.close()


# 检查是否有已下载、待上传文件
def check_tmp():
    tmp = open("tmp.txt", "r")
    tmp_info = tmp.readlines()
    tmp.close()
    if tmp_info:
        return True
    else:
        return False


# 获取已下载、待上传视频id
def get_tmp():
    tmp = open("tmp.txt", "r")
    tmp_info = tmp.readlines()
    tmp.close()
    return tmp_info[0][0:-1]


# 下载流程
def download_procedure(video_id):
    # 尝试下载所有文件，总共5次重试机会
    download_attempt = 1
    while True:
        if download_attempt > 5:
            logging.error("download fail after 5 attempts for {}".format(video_id))
            return False
        video_url = "https://www.youtube.com/watch?v={}".format(video_id)
        logging.info("start download {}".format(video_id))
        download_result = download(video_url)
        if download_result is False:
            logging.error("download error attempt {}".format(download_attempt))
            download_attempt += 1
            delete_procedure()
            time.sleep(LONG_GAP)
        else:
            break
    logging.info("download success {}".format(video_id))

    # # 将vtt字幕文件转换为srt格式
    # logging.info("start vtt2srt {}".format(video_id))
    # vtt2srt_result = vtt2srt()
    # if vtt2srt_result is False:
    #     logging.error("vtt 2 srt error")
    #     return False
    # logging.info("vtt2srt success {}".format(video_id))

    # 检查是否全部下载成功
    logging.info("start check download complete {}".format(video_id))
    download_complete_result = check_download_complete()
    if not download_complete_result:
        logging.error("download incomplete, something is missing")
        return False
    logging.info("check download success {}".format(video_id))
    return True


# 清理流程
def delete_procedure():
    # 删除下载产生的文件，保留.py .txt .log和chromedriver
    for file in os.listdir(os.getcwd()):
        if not (file.endswith(".py") or file.endswith(".txt") or file.endswith(".log") or file.endswith(".sh") or file == "chromedriver"):
            os.remove(os.getcwd() + "/" + file)
    logging.info("delete finish")


# 通知流程
def notify_procedure(result):
    # 将下载、上传结果通过邮件通知
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

    logging.info(">>>>>>>>>>>>>>>>>>>>  download job start  <<<<<<<<<<<<<<<<<<<<")
    if check_tmp():
        logging.error("video {} is uploading".format(get_tmp()))
        logging.info(">>>>>>>>>>>>>>>>>>>>  download job end  <<<<<<<<<<<<<<<<<<<<")
        sys.exit(1)
    delete_procedure()
    for username in target_youtube_user:
        video_list = find_all(username)
        for video_id in video_list:
            if not check_uploaded(video_id):
                start_time = time.time()
                logging.info("********** start downloading new video : {} **********".format(video_id))
                download_success = download_procedure(video_id)
                if not download_success:
                    logging.error("download fail {}".format(video_id))
                    end_time = time.time()
                    notify_procedure("下载youtube账户：'{}'\n\n视频：{}\n\n失败!\n\n共耗时 {}秒\n\n请检查！".format(username, video_id, end_time - start_time))
                    logging.info(">>>>>>>>>>>>>>>>>>>>  download job end  <<<<<<<<<<<<<<<<<<<<")
                    sys.exit(1)
                else:
                    write_tmp(video_id, username)
                    logging.info("video {} download and write to tmp success".format(video_id))
                    logging.info(">>>>>>>>>>>>>>>>>>>>  download job end  <<<<<<<<<<<<<<<<<<<<")
                    sys.exit(0)
    logging.info("no new video found")
    logging.info(">>>>>>>>>>>>>>>>>>>>  download job end  <<<<<<<<<<<<<<<<<<<<")
    sys.exit(1)
