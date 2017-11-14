#!/usr/bin/env python
# encoding: utf-8

"""
__author__: Widsom Zhang
__time__: 2017/11/13 18:32
"""
import json
import random
import urllib.request
from lxml import etree


def download_image(url, headers):
    """
    下载图片
    :param url: 图片的url
    :param headers: http的请求头
    :return:
    """
    # 截取图片的url
    lists = url.split('/')
    # 拼接图片保存的地址路径
    filename = 'image/' + lists[-1]
    # 将请求到的数据写入文件
    with open(filename, 'wb')as f:
        f.write(get_response(url, headers))


def write_image_url(url):
    """
    将图片的url写入文件
    :param url:
    :return:
    """
    # 以拼接的方式写入
    with open("imageurl.txt", 'a')as f:
        # 每写入一个换行
        f.write(url + "\n")


def get_response(url, headers):
    """
    获取响应对象
    :param url: 请求的url
    :param headers: 请求头信息
    :return: 返回服务器的响应信息
    """
    req = urllib.request.Request(url, headers=headers)
    resp = urllib.request.urlopen(req)
    return resp.read()


def parse_image(result):
    """
    解析html信息，获取image的url的策略
    :param result: html信息
    :return:
    """
    # 通过etree库将html信息转成对象
    html = etree.HTML(result)
    # 通过xpath解析规则，获取需要的图片url信息
    images = html.xpath('//li[@class="box"]/a/img/@src')
    for image in images:
        print(image)
        # 下载图片
        # download_image(image, headers)    # 下载图片太慢，这里注释了
        # 将图片的url写入文件
        write_image_url(image)


if __name__ == '__main__':
    """
        xpath爬虫示例：
        
            爬取的网站是：http://tu.duowan.com/m/bxgif
            
            使用fiddler软件抓包分析：
                在浏览器中输入上面的url，加载到30条需要的数据，随着滚动条往下拖动，数据再次加载且浏览器的url没有变化
                初步判断采用的是ajax框架加载数据，通过抓包工具找到加载的url。
                
            ajax加载的url：
                http://tu.duowan.com/m/bxgif?offset=30&order=created&math=0.2097926790117744
                url返回的json数据格式：
                {
                    "html": "...",
                    "more": true,
                    "offset": 60,
                    "enabled": true
                }
                http://tu.duowan.com/m/bxgif?offset=60&order=created&math=0.9387482944610999
                {
                    "html": "...",
                    "more": true,
                    "offset": 90,
                    "enabled": true
                }
                
                注：html字段是html中的"<li>..."的html数据，可以使用lxml和xpath解析，具体看代码
                
            通过查看html页面的源码，可以发现，offset是json数据返回的offset，order字段是固定的，math字段是一个（0,1）的随机数。
             
    """

    # 需要爬取的url
    url = 'http://tu.duowan.com/m/bxgif'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36'
    }
    # 将请求url的响应信息，通过xpath解析规则解析
    parse_image(get_response(url, headers))

    # 每次请求30条数据
    offset = 30
    more = True
    # 循环遍历30次，获取需要的数据（为什么是30，因为该网站数据不多，也就1000多）
    while more:
        # 拼接url
        url2 = 'http://tu.duowan.com/m/bxgif?offset=' + str(offset) + '&order=created&math=' + str(random.random())
        print(url2)
        result2 = get_response(url2, headers)
        # 解析json数据
        dict = json.loads(result2)
        # 获取html的value值
        result = dict['html']
        # offset的值
        offset = dict['offset']
        print(type(offset))
        print(str(offset))
        # 获取more的value值
        more = dict['more']
        # 如果more为true，表示有更多
        if more:
            # 解析image的url
            parse_image(result)
