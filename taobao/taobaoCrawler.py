from selenium import webdriver  # 通过代码控制与页面元素进行交互（点击、输入等）
import time
import random
import re
import urllib.request
import os


# step1: 查找商品，登录淘宝
def search_product(target):
    driver.find_element_by_id("q").send_keys(target)
    driver.find_element_by_class_name("btn-search").click()
    # driver.find_element_by_xpath('//*[@id="J_TSearchForm"]/div[1]/button').click()
    time.sleep(20)
    str = driver.find_element_by_xpath('//*[@id="mainsrp-pager"]/div/div/div/div[1]').text
    pages = int(re.compile('\d+').search(str).group(0))
    return pages


# step2: 拉取滑动条，把数据加载完毕
def drop_down():
    for x in range(1, 11, 2):
        time.sleep(random.uniform(0.5, 2))
        j = x / 10
        js = 'document.documentElement.scrollTop = document.documentElement.scrollHeight * %f' % j
        driver.execute_script(js)


# step3: 采集数据
def download(url, file_path):
    if url.find(".jpg") > 1:
        temp = url.split(".jpg")
        url = temp[0] + '.jpg'
        print(url)

    file_path = file_path + '/' + url.split("/")[-1]
    if not os.path.exists(file_path):
        request = urllib.request.Request(url)
        response = urllib.request.urlopen(request)
        get_img = response.read()
        with open(file_path, "wb") as f:
            f.write(get_img)


def get_products(file_path):
    lis = driver.find_elements_by_xpath('//div[@class="items"]/div[@class="item J_MouserOnverReq  "]')
    for li in lis:
        image_url = li.find_element_by_xpath('.//div[@class="pic"]/a/img').get_attribute('src')
        # print(image_url)
        download(image_url, file_path)


# step4: 下一页
# 模拟翻页会被检测到，所以采取用URL访问下一页或者手动输入页码跳转页码
def next_page(target, num):
    driver.get('https://s.taobao.com/search?q={}&s={}'.format(target, 44 * num))
    driver.implicitly_wait(10)



if __name__ == '__main__':
    target = '双胞胎装'#搜索目标
    file_path = 'img'+'/'+target#存储路径

    driver = webdriver.Chrome(r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
    driver.get('https://www.taobao.com')

    pages = search_product(target)
    for num in range(pages):
        drop_down()
        get_products(file_path)
        next_page(target, num + 1)
