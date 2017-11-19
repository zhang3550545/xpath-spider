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


def get_headers():
    """
    随机获取请求头的User-Agent
    :return:
    """
    list = [
        {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0.1; Galaxy Nexus Build/IMM76B) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Mobile Safari/535.19'},
        {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36'},
        {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36'},
        {'User-Agent': 'Mozilla/5.0(WindowsNT6.1;rv:2.0.1)Gecko/20100101Firefox/4.0.1'},
        {
            'User-Agent': 'Agent:Mozilla/5.0(Macintosh;IntelMacOSX10_7_0)AppleWebKit/535.11(KHTML,likeGecko)Chrome/17.0.963.56Safari/535'},
        {'User-Agent': 'Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1;TencentTraveler4.0)'},
        {
            'User-Agent': 'Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1;Trident/4.0;SE2.XMetaSr1.0;SE2.XMetaSr1.0;.NETCLR2.0.50727;SE2.XMetaSr1.0)'},
        {
            'User-Agent': ':Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1;Trident/4.0;InfoPath.2;.NET4.0C;.NET4.0E;.NETCLR2.0.50727;360SE)'}
    ]

    index = random.randint(0, len(list) - 1)
    return list[index]


def get_headers2(full_url):
    """
    因为在获取图片的实际信息，需要将full_url作为请求头传入
    :param full_url: 套图子页面的url
    :return: 返回一个headers
    """
    headers = {
        'User-Agent': 'Agent:Mozilla/5.0(Macintosh;IntelMacOSX10_7_0)AppleWebKit/535.11(KHTML,likeGecko)Chrome/17.0.963.56Safari/535',
        'Referer': full_url
    }
    return headers


def get_image_nums(soup):
    """
    获取套图的数量
    :param soup:
    :return: 返回套图的总数
    """
    return int(soup.select('div[class="column"]')[0].span.string.split('.')[0])


def get_image_url(soup):
    """
    获取子页面的图片url
    :param soup: BeautifulSoup对象，解析，获取图片的url
    :return: 返回图片的url
    """
    return soup.select('div[id="picbox"]')[0].img['src']


def load_image(file_dir, image_url):
    """
    加载图片，并保存本地
    :param file_dir: 本地存储路径
    :param image_url: 图片的url
    :return:
    """
    print(image_url)
    # 图片的url写入文件
    wirte_url('cache/image_url.txt', image_url)
    # 拼接图片保存的文件名
    filename = file_dir + "/" + image_url.split('/')[-1]
    # 没有文件路径，创建一个
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    # 将图片写入文件
    with open(filename, 'wb') as f:
        f.write(get_response_file(image_url))


def wirte_url(filename, image_url):
    """
    将图片的url写入文件
    :param image_url: 图片的url
    :return:
    """
    with open(filename, 'a')as f:
        f.write(image_url + "\n")


def is_load_url(url):
    cache_file = 'cache/page_url.txt'
    with open(cache_file, 'r') as f:
        if url in str(f.readlines()):
            return True
    return False


def create_filedir(soup):
    """
    获取文件的保存本地的路径
    :param soup: BeautifulSoup对象，用来解析page的数据
    :return:
    """
    filename = 'image/'
    filename = filename + soup.select('div[class="column"]')[0].a.string
    contents = soup.select('meta[name="keywords"]')[0]['content'].split(',')

    if len(contents) > 0:
        filename = filename + "/" + contents[0]
    if len(contents) > 1:
        filename = filename + "/" + contents[1]

    filename = filename + '/' + soup.title.string.split('_')[0]
    return filename


def get_response(url, headers=None):
    """
    请求url，获取response结果,返回一个文本
    :param url: 请求的url
    :param headers: headers字段，可以自定义
    :return: 返回响应的结果
    """
    # 随机休眠1-5秒
    time.sleep(random.randint(1, 5))
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
    time.sleep(random.randint(1, 5))
    response = session.get(url, headers=get_headers())
    return response.content


def load_child_page(url):
    """
    加载子页面，子页面有我们需要的图片
    :param url: 子页面的url
    :return:
    """
    # 获取soup对象
    soup = get_soup(url)
    # 获取图片文件的本地存储目录
    file_dir = create_filedir(soup)
    # 获取图片的数量
    nums = get_image_nums(soup)
    # 遍历，获取每一张图片，因为每一个页面，只有一张我们需要的图片
    for num in range(1, nums + 1):
        # 拼接子页面的url
        full_url = url + "?url=" + str(num)
        # 图片是通过子页面的下面的url链接返回，所以拼接url，请求图片数据
        load_image_url = "http://www.99mm.me/url.php?id=" + url.split('/')[-1].split('.')[0]
        # 获取图片数据
        text = get_response(load_image_url, get_headers2(full_url))
        # 解析图片数据
        for image_url in text.split('"'):
            # 过滤我们需要的数据
            if 'http:' in image_url and str(num) == image_url.split('/')[-1].split('-')[0]:
                # 加载图片
                load_image(file_dir, image_url)


def load_guide_page(url):
    """
    加载向导页
    :param url:
    :return:
    """
    soup = get_soup(url)
    for item in soup.select('ul[id="piclist"]')[0].find_all('dt'):
        child_page_url = "http://www.99mm.me" + item.a['href']
        load_child_page(child_page_url)
        wirte_url('cache/page_url.txt', child_page_url)

    parse_pre_page(soup)


def parse_pre_page(soup):
    """
    解析向导页的下一页
    :param soup:
    :return:
    """
    next_list = soup.select('div[class="page"]')[0].select('a[class="next"]')
    full_url = 'http://www.99mm.me/hot/'
    if len(next_list) > 0:
        short_url = next_list[0]['href']
        if 'http://' in short_url:
            full_url = short_url
        else:
            full_url = full_url + short_url
        load_guide_page(full_url)


def get_soup(url):
    """
    返回一个BeautifulSoup对象
    :param url:
    :return:
    """
    # 使用lxml解析
    return BeautifulSoup(get_response(url), 'lxml')


if __name__ == '__main__':
    """
    首页：
        url = 'http://www.99mm.me'
        
        <ul id="piclist">
            <li>
                <dl>
                    <dt><a href="/qingchun/2644.html" target="_blank"><img src="http://img.99mm.net/small/2017/2644.jpg" width="636" alt="短发妹波菲高耸雪白的美胸画面美不胜收"/></a></dt>
                    <dd><a href="/qingchun/2644.html" target="_blank">短发妹波菲高耸雪白的美胸画面美不胜收</a></dd>
                </dl>
            </li>
            ...
        </ul>
        
        解析子页面
                
        <div class="page">
            <a href="/hot/" class="pre">上一页</a>
            <a href="/hot/">1</a><em>2</em>
            <a href="mm_4_3.html">3</a>
            <a href="mm_4_4.html">4</a>
            <a href="mm_4_5.html">5</a>
            <a href="mm_4_6.html">6</a>
            <a href="mm_4_7.html">7</a>
            <a href="mm_4_8.html">8</a>
            <a href="mm_4_67.html" class="all">...67</a>
            <a href="mm_4_3.html" class="next">下一页</a>
        </div>
        
        解析下一个页面
    
    子页面：
        
        <title>短发妹波菲高耸雪白的美胸画面美不胜收_九妹图社</title>
        <meta name="keywords" content="魅妍社,波菲"/>
        
        <div class="column"><span>38.P</span><a href="/qingchun/">清纯</a></div>
        
        <div id="picbox"><img src="http://img.99mm.net/2017/2644/1-wx.jpg" alt="短发妹波菲高耸雪白的美胸画面美不胜收"/></div>
        
        base_url='http://www.99mm.me'
        
        图片存储目录：image/清纯/魅妍社/波菲短发妹波菲高耸雪白的美胸画面美不胜收/1-wx.jpg
    
    """
    session = requests.session()
    url = 'http://www.99mm.me'
    load_guide_page(url)

    pass
