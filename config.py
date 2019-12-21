import  configparser

import  os,sys,platform

class Config:
    def __init__(self,file_path:str):
        self.fp=file_path
        self.read_config()




    def read_config(self):
        '''
        从文件中读取配置
        :return:
        '''
        if not os.path.exists(self.fp):
            self.fp_status = False
            return

        self.conf = configparser.ConfigParser()
        self.conf.read(self.fp,encoding="utf-8")
        self.fp_status = True



    def __get_sections(self):
        '''
        获取所有的section
        :return:
        '''
        if self.fp_status:
            self.secs = self.conf.sections()

        else:
            self.secs=[]

    def set_setcion_items(self,section_name,pwd,type):
        self.conf.set(section_name,"password",pwd)
        self.conf.set(section_name, "auto_login", str(type))
        self.save()

    def get_account_type(self,section_name):
        '''
        获取是否记住密码的点
        :param section_name:
        :return:
        '''
        try:
            return self.conf.get(section_name,"auto_login")
        except Exception as e:
            return 0

    def set_new_section(self,username,pwd,type):
        self.conf.clear()
        self.conf[username]={
            "password":pwd,
            "auto_login":type
        }
        self.save()

    def get_pwd(self,section_name):
        '''
        获取密码，
        :param section_name: section，就是用户的名字
        :return:
        '''
        try:
            return self.conf.get(section_name,"password")
        except Exception as e:
            return ""


    def sections(self):
        self.__get_sections()
        return  self.secs


    def save(self):
        '保存到配置文件中'
        with open(self.fp, 'w') as f:
            self.conf.write(f)



class Utils:
    '''
    工具类
    '''
    @staticmethod
    def get_config_path()->str:
        '''
        获取pyqt打包后的临时文件
        :return:
        '''
        if hasattr(sys, '_MEIPASS'):
            # # # PyInstaller会创建临时文件夹temp，并把路径存储在_MEIPASS中
            # # appPath = os.path.dirname(os.path.realpath(sys.executable))
            # # print(appPath)
            # # cf = configparser.ConfigParser()
            # buf = cf.read(filenames=sys._MEIPASS)

            return sys._MEIPASS

        return None

    @staticmethod
    def get_system()->str:
        '''
        获取当前系统
        :return:
        '''
        if "Windows" in platform.version():

            return "WIN"
        else:
            # 非window下路径格式都一样
            return "N"




if __name__ =="__main__":
    path = "/Users/freedom/Documents/Sync/PCSync/Codes/py_code/wifi.bmstu.ru/bmstu_pwd.cfg"
    c = Config(path)
