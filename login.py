
import requests

import sys, os,platform

'''
记得判断是否处于联网状态
'''

import re,random

import  time

from datetime import datetime

import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


from user_agents import  user_agents

headers={
    "Content-Type":"application/x-www-form-urlencoded",
    "Origin":"https://internet.msfu.ru",
    "Accept-Encoding":"br, gzip, deflate",
    "Connection":"keep-alive",
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "User-Agent":random.choice(user_agents),
    "Referer":"https://internet.msfu.ru/login",
}


def login_print(err_msg):
    print("{}:{}".format(datetime.now(),err_msg))

def login_post(username:str,pwd:str,dst="https://www.google.com/"):

    #login_url = "https://internet.msfu.ru/login"
    login_url = "https://internet.msfu.ru/logout"
    args = {
        "dst": dst,
        "popup": True,
        "username": username,
        "password": pwd,
    }

    worong_note=r"Неверное имя пользователя или пароль"
    re_pattern = re.compile(worong_note)

    try:

        recv_status = requests.post(url=login_url,data=args,headers=headers,verify=False,timeout=5)
        recv_status.encoding=recv_status.apparent_encoding
        wrong_flag = re.findall(re_pattern,recv_status.text)

        if len(wrong_flag)==0:
            return True
        else:
            raise

        # print(recv_status.status_code)
        #
        # print(recv_status.content)
        # print(recv_status.text)

    except Exception as e:
        # 如果错误码是403，就说明用的不是мгту的网
        return False

def statcs_check()->bool:
    need_login=r"Вы подключены через ЛС"
    re_pattern = re.compile(need_login)

    try:

        recv = requests.get("https://www.google.com",verify=False,timeout=10)
        recv.encoding = recv.apparent_encoding
        wrong_list = re.findall(re_pattern, recv.text)

        if len(wrong_list)!=0:
            login_print("检测到账号退出")
            raise
        else:
            return True

    except Exception as e:
        print(e)
        #如果是这种的就是没联网
        "Failed to establish a new connection"
        return False


def title():
    print("keep МГТУ network online ")
    print("version 0.01")
    print("wechatID crazysaturday")






if __name__=="__main__":

    title()



    try:

        while 1:
            login_status = login_post("mop", "18301919")
            net_stats=statcs_check()
            if net_stats:
                #print("无须登录")
                time.sleep(5)
            else:

                login_print("账户登录中")

                login_status=login_post("mop", "18301919")

                if not login_status:

                    raise IOError

                login_print("登录成功")

                login_print("*"*20)

    except IOError:
        login_print("登录失败，账号或密码失败,或请检查网络链接状态")
        exit(-1)
    except KeyboardInterrupt:
        login_print("退出成功")
        exit(0)

