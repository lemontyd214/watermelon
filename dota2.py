import requests
import time


def login():
    header = {
        "accept": "text/javascript, text/html, application/xml, text/xml, */*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,sv;q=0.8,en;q=0.7",
        "cookie": "passport_csrf_token=eaad9fb9140ad4b0dc2eebef1b155bb7; sso_auth_status_ss=bbcf5b9313eec89419124924e67bed03; passport_auth_status_ss=67887260d9a9a23d1bdc94dd9daa1006%2Ceeb67ecf59036f6a284c61bf5def9782; toutiao_sso_user_ss=5e86424945f1b2408584cc565728c704; uid_tt_ss=30a9cf9a1f754f661c94b1b5e7464c23; sessionid_ss=5e86424945f1b2408584cc565728c704; sso_uid_tt_ss=3f43a81895363d4a642bf9827f476625",
        "origin": "https://www.ixigua.com",
        "referer": "https://www.ixigua.com/",
        "sec-ch-ua": '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
        "sec-ch-ua-mobile": "?0",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"
    }

    form_data = {
        "aid": "1768",
        "host": "https://sso.toutiao.com",
        "service": "https://www.ixigua.com/?is_new_connect=0&is_new_user=0",
        "account_sdk_source": "sso",
        "ttwid": "6990548260651042318",
        "mix_mode": "1",
        "fp": "verify_krprc8x5_gkpYaTsl_ov8f_4dQg_AL29_yhu3xkZDIvAS",
        "account": "2e3d3334313235343537343d3136",
        "password": "717c343c3c31373431",
        "timestamp": str(int(time.time()*1000))
    }

    login_url = "https://sso.toutiao.com/account_login/v2/"
    res = requests.post(login_url, headers=header, params=form_data, allow_redirects=False, verify=False)
    print(res.text)
    login_url = res.text.split('"')[9]
    print(login_url)
    print(login_url.split('=')[2])
    login_params = {
        "next": "https://www.ixigua.com/?is_new_connect=0&is_new_user=0",
        "ticket": login_url.split('=')[2]
    }
    r = requests.get(login_url, params=login_params)
    # print(r.text)
    print("login success")


if __name__ == "__main__":
    login()