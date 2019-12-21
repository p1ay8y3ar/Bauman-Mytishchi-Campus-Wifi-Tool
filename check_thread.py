
from PyQt5.QtCore import  QThread,pyqtSignal

from user_agents import user_agents
import  random,re,requests,time


#禁止显示错误行
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class LoginUitl:

    def __init__(self,username,pwd):
        self.UA=user_agents  #获取各种的header

        self.username=username
        self.pwd=pwd

        self.login_url = "https://internet.msfu.ru/login"
        self.logout_url = "https://internet.msfu.ru/logout"

    def __get_ua(self)->str:
        '''
         获取一个header
        :return:
        '''
        return random.choice(self.UA)

    def get_header(self)->dict:
        '''
        产生一个header
        :return:
        '''
        return {
            "Content-Type": "application/x-www-form-urlencoded",
            "Origin": "https://internet.msfu.ru",
            "Accept-Encoding": "br, gzip, deflate",
            "Connection": "keep-alive",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "User-Agent": self.__get_ua(),
            "Referer": "https://internet.msfu.ru/login",
        }

    def check_networkstatus(self):
        need_login = r"Вы подключены через ЛС"
        re_pattern = re.compile(need_login)

        try:

            urlist=['https://yandex.ru/search/',"https://www.google.com"]
            recv = requests.get(random.choice(urlist), verify=False, timeout=10)
            recv.encoding = recv.apparent_encoding
            wrong_list = re.findall(re_pattern, recv.text)

            if len(wrong_list) != 0:
                # 账号退出
                raise
            else:
                return "S"

        except Exception as e:
            # 如果是这种的就是没联网

            for i in e.args:
                if type(i)==urllib3.exceptions.MaxRetryError:
                    return "N"

            return "F"



    def logout(self):

        '''
        退出函数，需要重新进行判断
        :return:
        '''

        # 主要登录了账户,不管账号密码是不是正确，都会退出
        return  self.post_data(self.logout_url)

    def login(self):
        return self.post_data(self.login_url)


    def post_data(self,url,dst="https://www.google.com/",):

        args = {
            "dst": dst,
            "popup": True,
            "username": self.username,
            "password": self.pwd,
        }

        worong_note = r"Неверное имя пользователя или пароль"
        re_pattern = re.compile(worong_note)
        try:

            recv_status = requests.post(url=url, data=args, headers=self.get_header(), verify=False, timeout=5)
            recv_status.encoding = recv_status.apparent_encoding
            wrong_flag = re.findall(re_pattern, recv_status.text)

            #对状态进行判断
            if recv_status.status_code==403:
                # 如果错误码是403，就说明用的不是мгту的网
                return "N"
            if len(wrong_flag) == 0:
                return "S"
            else:
                raise

        except Exception as e:

            return "F"



class NetWorkThread(QThread):

    _status_signal = pyqtSignal(str)

    def __init__(self, username,pwd,parent=None):
        super(NetWorkThread, self).__init__()

        #赋值 用户账号和密码
        self.username =username
        self.pwd=pwd

        #初始化登录程序
        self.LT = LoginUitl(username=self.username,pwd=self.pwd)

        self._stop_flag =False

    def logout(self):
        logou_status = self.LT.logout()
        if logou_status == "N":
            return "please connect to BMSTU's network", False
        else:
            return "logout success", True


    def __del__(self):
        self.wait()

    def set_thread_status(self,bo):
        self._stop_flag=bo


    def first_check(self):

        '''
        对网络登录状态进行判断
        1:检查网络连接状态
            没有联网
            连的不是bm的网
        2:进行重新登录，以此来判断账号密码是不是正确

        :return:
        '''
        net_work_status = self.LT.check_networkstatus()
        if net_work_status=="N": #说明网络可能没有连接
            return "please check network connect status",False
        elif net_work_status =="S":# 说明已经登录了，那就先退出账号
            logou_status = self.LT.logout()
            if logou_status=="N":
                return "please connect to BMSTU's network",False

        #进行账号密码的登录
        login_status = self.LT.login()
        if login_status=="F":
            return  "wrong username or password",False
        elif login_status=="N":
            return "please connect to BMSTU's network", False

        return "login success",True



    def run(self):

        random_sleeptime = [1,2,3,4]

        while not self._stop_flag:
            #进行登录检测的主要部分
            net_work_status =  self.LT.check_networkstatus()
            if net_work_status == "N":  # 说明网络可能没有连接
                self._status_signal.emit("W")
                break
            elif net_work_status=="S":
                ''' 说明账号处于登录状态 '''
                time.sleep(random.choice(random_sleeptime))
            else:
                #说明账号退出了，进行账号的登录

                # 进行账号密码的登录
                login_status = self.LT.login()
                if login_status == "F":
                    self._status_signal.emit("F")

                elif login_status == "N":
                    # 网络状态错误
                    self._status_signal.emit("W")
                    break
                else :
                    self._status_signal.emit("S")#登录成功

        self.logout()
        self._status_signal.emit("E")  # 退出循环






