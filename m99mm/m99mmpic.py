#!/usr/bin/env python
# encoding: utf-8

"""
__author__: Widsom Zhang
__time__: 2017/11/18 23:01
"""
import random
import os
import requests
import time
from bs4 import BeautifulSoup

list = [
    'Mozilla/5.0 (Linux; Android 6.0.1; Galaxy Nexus Build/IMM76B) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Mobile Safari/535.19',
    'Mozilla/5.0 (Linux; Android 5.1.1; XiaoMi4 Build/IMM76B) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Mobile Safari/535.19',
    'Mozilla/5.0 (Linux; Android 6.0.1; XiaoMi6 Build/IMM76B) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Mobile Safari/535.19',
    'Mozilla/5.0 (Linux; Android 7.0.0; RedMi3 Nexus Build/IMM76B) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Mobile Safari/535.19',
    'Mozilla/5.0 (Linux; Android 6.0.1; Nexus6 Build/IMM76B) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Mobile Safari/535.19'
]


def get_headers():
    """
    随机获取请求头的User-Agent
    :return:
    """
    index = random.randint(0, len(list) - 1)
    headers = {'User-Agent': list[index]}
    return headers


def get_response(url, headers=None):
    """
    请求url，获取response结果,返回一个文本
    :param url: 请求的url
    :param headers: headers字段，可以自定义
    :return: 返回响应的结果
    """
    # 随机休眠1-5秒
    time.sleep(random.randint(1, 3))
    if headers is None:
        headers = get_headers()
    response = session.get(url, headers=headers)
    # 解码之后返回，因为有中文乱码问题
    return response.text.encode('latin1').decode('utf-8')


def get_response_file(url):
    """
    请求url，返回一个二进制的响应信息
    :param url: 请求的url
    :return: 返回二进制数据
    """
    # 随机休眠1-5秒
    time.sleep(random.randint(1, 3))
    response = session.get(url, headers=get_headers())
    return response.content


def get_soup(url):
    """
    返回一个BeautifulSoup对象
    :param url:
    :return:
    """
    # 使用lxml解析
    return BeautifulSoup(get_response(url), 'lxml')


def get_image_url(soup):
    """
    获取子页面的图片url
    :param soup: BeautifulSoup对象，解析，获取图片的url
    :return: 返回图片的url
    """
    return soup.select('div[id="picbox"]')[0].img['src']


def get_next_page_url(soup):
    list = soup.select('div[id="picbox"]')[0].a['href'].split('=')
    if len(list) > 1:
        return list[-1]
    else:
        return ""


def create_filedir(soup):
    """
    获取文件的保存本地的路径
    :param soup: BeautifulSoup对象，用来解析page的数据
    :return:
    """
    filename = 'image'
    contents = soup.select('meta[name="keywords"]')[0]['content'].split(',')
    if len(contents) > 0:
        filename = filename + "/" + contents[0]
    if len(contents) > 1:
        filename = filename + "/" + contents[1]
    filename = filename + '/' + soup.select('title')[0].text.replace("九妹图社", "")
    return filename


def wirte_image_url(filename, image_url):
    """
    将图片的url写入文件
    :param image_url: 图片的url
    :return:
    """
    with open(filename, 'a')as f:
        f.write(image_url + "\n")


def load_image(file_dir, image_url):
    """
    加载图片，并保存本地
    :param file_dir: 本地存储路径
    :param image_url: 图片的url
    :return:
    """
    print(image_url)
    # 图片的url写入文件
    wirte_image_url('cache/image_url.txt', image_url)
    # 拼接图片保存的文件名
    filename = file_dir + "/" + image_url.split('/')[-1]
    # 没有文件路径，创建一个
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    # 将图片写入文件
    with open(filename, 'wb') as f:
        f.write(get_response_file(image_url))


def load_child_page(url):
    """
    加载子页面，子页面有我们需要的图片
    :param url: 子页面的url
    :return:
    """
    if "?url=" not in url:
        url = url + "?url=1"

    print(url)

    # 获取soup对象
    soup = get_soup(url)
    # 获取图片文件的本地存储目录
    file_dir = create_filedir(soup)
    # 获取当前页面的图片url
    image_url = get_image_url(soup)
    # 加载图片
    load_image(file_dir, image_url)
    # 拼接下一页图片
    part_url = get_next_page_url(soup)
    if "" != part_url:
        next_url = url.split('=')[0] + "=" + part_url
        load_child_page(next_url)


def get_guide_next_page_url(soup):
    tag = soup.select('li[class="next"]')[0].a
    if tag is None:
        return None
    else:
        return "http://m.99mm.me" + tag['href']


def load_guide_page(url):
    """
    加载向导页
    :param url:
    :return:
    """
    print(url)
    soup = get_soup(url)
    for tag in soup.select('div[class="pic"]'):
        child_page_url = "http://m.99mm.me" + tag.select('a')[0]['href']
        print(child_page_url)
        load_child_page(child_page_url)
        wirte_image_url('cache/page_url.txt', child_page_url)

    next_guide_url = get_guide_next_page_url(soup)
    if next_guide_url is not None:
        load_guide_page(next_guide_url)
    else:
        print("-------end--------")


if __name__ == '__main__':
    """
    首页：
        url = http://m.99mm.me/home/1.html
    
    
    子页面：
        
        <title>妩媚美人李丽莎浑圆完美的身材难以抗拒九妹图社</title>

        <meta name="keywords" content="头条女神,李丽莎"/>
        
        <div id="picbox"><a href="2645.html?url=3"><img src="http://img.99mm.net/2017/2645/2-zd.jpg" alt="妩媚美人李丽莎浑圆完美的身材难以抗拒(2)"/></a></div>
        
        base_url='http://m.99mm.me/meitui/2645.html?url=3'
        
        图片存储目录：image/头条女神/李丽莎/妩媚美人李丽莎浑圆完美的身材难以抗拒/2-zd.jpg
    
    """
    session = requests.session()
    url = 'http://m.99mm.me/home/1.html'
    load_guide_page(url)
