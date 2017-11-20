#!/usr/bin/env python
# encoding: utf-8

"""
__author__: Widsom Zhang
__time__: 2017/11/20 15:03
"""

import requests
from bs4 import BeautifulSoup


def get_headers():
    return {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36'
    }


def write_html(text, filename):
    """
    将返回的响应信息写入文件
    :param text: 响应页面内容
    :param filename:   保存的文件名
    :return:
    """
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(text)


if __name__ == '__main__':
    # csdn登入的url
    login_url = "https://passport.csdn.net/account/login"
    # 通过requests的session请求
    seesion = requests.session()
    # 通过get请求登录页面的url，获取响应数据
    response = seesion.get(login_url, headers=get_headers())
    # 输出响应码
    print(response.status_code)
    # 将返回的html写入文件
    write_html(response.text, 'get_login.html')

    # 使用BeautifulSoup解析html，使用lxml的方式解析
    soup = BeautifulSoup(response.text, 'lxml')
    # 获取登入页面的input标签中lt的值，后面post表单上传登入信息需要
    lt = soup.select('input[name="lt"]')[0]['value']
    # 获取登入页面的input标签中execution的值，后面post表单上传登入信息需要
    execution = soup.select('input[name="execution"]')[0]['value']
    # 上传表单的data数据
    data = {
        "username": "your-username",
        "password": "your-password",
        "lt": lt,
        "execution": execution,
        "_eventId": "submit"
    }

    # 打印data数据
    print(data)

    # post请求上传data数据，模拟登入，获取响应结果
    response = seesion.post(login_url, data=data, headers=get_headers())
    # 打印响应的状态码
    print(response.status_code)
    # 将响应的信息写入文件
    write_html(response.text, 'login_success.html')

    # 通过get请求，请求个人主页，如果没有登入成功，则会返回登页，登入成功，则会获取到登入的个人信息
    response = seesion.get('https://my.csdn.net/my/mycsdn', headers=get_headers())
    # 打印响应码
    print(response.status_code)
    # 将响应结果保存文件
    write_html(response.text,'my.html')
