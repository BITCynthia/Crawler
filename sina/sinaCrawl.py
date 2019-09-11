import sinaLogin as sl
import time
import random
from bs4 import BeautifulSoup
import os
import urllib.request

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,ja;q=0.8,en;q=0.7,zh-TW;q=0.6',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Referer': 'https://weibo.com/?sudaref=www.baidu.com&display=0&retcode=6102',
    'Connection': 'keep-alive'
}


# 初次会话
def get_session(session, target):
    time.sleep(random.uniform(2, 4))
    return session.post(
        "https://s.weibo.com/weibo?q={}&typeall=1&haspic=1&Refer=g&page=1".format(target), verify=False, headers=header)


# 翻页
def get_data_session(session, target, page):
    time.sleep(random.uniform(2, 4))
    return session.post(
        "https://s.weibo.com/weibo?q={}&typeall=1&haspic=1&Refer=g&page={}".format(target, page), verify=False,
        headers=header)


# 初次会话，获取页码
def get_page_res(session, target):
    try:
        return get_session(session, target)
    except:
        try:
            return get_session(session, target)
        except:
            print("获取页码信息失败")
            return 0


# 翻页读取页面信息
def get_data_res(session, target, page):
    try:
        return get_data_session(session, target, page)
    except:
        try:
            return get_data_session(session, target, page)
        except:
            print("获取页面数据失败")
            return 0


# 获取页码
def get_page(session, target):
    response = get_page_res(session, target)
    if response:
        try:
            soup = BeautifulSoup(response.text, "html.parser")
            pages = soup.find("ul", "s-scroll").find_all("li")
            return len(pages)
        except:
            print("获取页码失败")
            return 0


def download(url, file_path):
    temp = url.split("/")
    # print(temp)
    url = "https://" + temp[2] + "/bmiddle/" + temp[4]
    print(url)

    file_path = file_path + '/' + url.split("/")[-1]
    print(file_path)
    if not os.path.exists(file_path):
        request = urllib.request.Request(url)
        reponse = urllib.request.urlopen(request)
        get_img = reponse.read()
        with open(file_path, "wb") as f:
            f.write(get_img)
    return


# 读取页面信息
def get_data(session, target, page, file_path):
    response = get_data_res(session, target, page)
    if response:
        try:
            soup = BeautifulSoup(response.text, "html.parser")
            # print(soup.title)
            uls = soup.find_all('ul', attrs={"class": "m3"})
            for ul in uls:
                # print(ul)
                imgs = ul.find_all('img')
                for img in imgs:
                    # print(img)
                    url = img.get('src')
                    print(url)
                    download(url, file_path)

        except:
            print("获取页面图片失败")
            return 0


if __name__ == '__main__':
    target = '情侣拍照'
    file_path = 'sina' + '/' + target

    session = sl.main()
    # 获取页码
    pages = get_page(session, target)
    # print(pages)
    # 获取页面图片
    for page in range(pages):
        print(get_data(session, target, page, file_path))
