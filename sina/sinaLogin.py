import requests
import urllib
import base64
import time
import re
import json
import rsa
import binascii
from bs4 import BeautifulSoup

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,ja;q=0.8,en;q=0.7,zh-TW;q=0.6',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Referer': 'https://weibo.com/?sudaref=www.baidu.com&display=0&retcode=6102',
    'Connection': 'keep-alive'
}


class Login(object):
    session = requests.session()
    user_name = "**********"
    pass_word = "**********"

    def get_username(self):
        # requests.su = sinaSSOEncoder.base64.encoder(urlencode(username))
        return base64.b64encode(urllib.parse.quote(self.user_name).encode("utf-8")).decode("utf-8")

    def get_pre_login(self):
        params = {
            "entry": "weibo",
            "callback": "sinaSSOController.preloginCallBack",
            "su": self.get_username(),
            "rsakt": "mod",
            "checkpin": "1",
            "client": "ssologin.js(v1.4.18)",
            "_": int(time.time() * 1000)
        }
        try:
            response = self.session.post("https://login.sina.com.cn/sso/prelogin.php", params=params, headers=header,
                                         verify=False)
            # print(response.text)
            return json.loads(re.search(r"\((?P<data>.*)\)", response.text).group(("data")))
        except:
            print("获取公钥失败！")
            return 0

    def get_password(self):
        public_key = rsa.PublicKey(int(self.get_pre_login()["pubkey"], 16), int("10001", 16))
        password_string = str(self.get_pre_login()["servertime"]) + '\t' + str(
            self.get_pre_login()["nonce"]) + '\n' + self.pass_word
        password = binascii.b2a_hex(rsa.encrypt(password_string.encode("utf-8"), public_key)).decode("utf-8")
        # print(password)
        return password

    def login(self):
        post_data = {
            "entry": "sso",
            "gateway": "1",
            "from": "",
            "savestate": "30",  #
            "qrcode_flag": "false",
            "userticket": "1",
            "vsnf": "1",
            "su": self.get_username(),
            "service": "sso",
            "servertime": self.get_pre_login()["servertime"],
            "nonce": self.get_pre_login()["nonce"],
            "pwencode": "rsa2",
            "rsakv": self.get_pre_login()["rsakv"],
            "sp": self.get_password(),
            "sr": "1440*960",
            "encoding": "UTF-8",
            "prelt": "17",
            "url": "https://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack",
            "returntype": "TEXT"
        }
        login_data = self.session.post("https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)",
                                       data=post_data, headers=header, verify=False)
        # print(login_data.json())
        params = {
            "ticket": login_data.json()['ticket'],
            "ssosavestate": int(time.time()),
            "callback": "sinaSSOController.doCrossDomainCallBack",
            "scriptID": "ssoscript0",
            "client": "ssologin.js(v1.4.18)",
            "_": int(time.time() * 1000)
        }
        self.session.post("https://passport.weibo.com/wbsso/login", params=params, headers=header, verify=False)
        return self.session


def main():
    login = Login()
    session = login.login()
    response = session.post("https://weibo.com", verify=False, headers=header)
    soup = BeautifulSoup(response.text, "html.parser")
    print(soup.find('title'))
    return session


if __name__ == '__main__':
    main()
