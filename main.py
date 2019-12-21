from PyQt5.QtWidgets import QMainWindow, QSystemTrayIcon, QApplication,QMenu,QAction,QMessageBox,qApp
from PyQt5.QtGui import QIcon,QPixmap,QPalette,QBrush,QCursor
from PyQt5.QtCore import  QSize,QThread,pyqtSignal,QEvent,Qt

import  sys
import  time
from UI.bmstu_login import Ui_Form
from datetime import datetime
from d11 import  *

from config import  Config,Utils,os

from check_thread import  NetWorkThread

class BMSTU_NT(QMainWindow, Ui_Form):

    def __init__(self):
        QMainWindow.__init__(self)
        Ui_Form.__init__(self)
        self.setupUi(self)

        self.m_drag = False #定义一个拖动窗口的标志

        self.__some_init()
        self.info_label.hide()
        # 禁止窗口放大和拉伸,设置为frame的长宽
        geometry=self.geometry() #获取窗口的长宽
        # 设置窗口长度，禁止拉伸
        self.setFixedSize(geometry.width(), geometry.height())
        # 背景透明


        self.setAttribute(Qt.WA_TranslucentBackground, True)
        # 无边框

        self.setWindowFlags(Qt.FramelessWindowHint)  # 隐藏边框
        # 禁止最大化
        # 鼠标跟踪

        self.setMouseTracking(True)
        #self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)
        # 设置标题
        self.setWindowTitle("МГТУ общежите")

        #槽函数关联
        self.btn_login.clicked.connect(self.onbtn_clicked_login)

        # 添加状态栏按钮
        self._addmenu()

        self.set_editline_information()



    def set_editline_information(self):

        # 开始进行数据操作
        # 获取程序的运行地址，
        config_base_path = Utils.get_config_path()

        if config_base_path == None:
            config_base_path, file_name = os.path.split(os.path.abspath(__file__))

        if "WIN" == Utils.get_system():
            configfile_path = config_base_path + r"\bmstu_pwd.cfg"
        else:
            configfile_path = config_base_path + r"/bmstu_pwd.cfg"
        print(configfile_path)

        self.config = Config(configfile_path)

        user_list = self.config.sections()

        if len(user_list)==0:
            return

        username = user_list[0]

        login_statu = int(self.config.get_account_type(username))

        if login_statu ==0:
            return
        else:
            self.remberme.setChecked(True)

        user_pwd = self.config.get_pwd(username)

        self.lineEdit_name.setText(username)
        self.lineEdit_pwd.setText(user_pwd)




    def onbtn_clicked_login(self):

        self.login_name =self.lineEdit_name.text()
        self.login_pwd  =self.lineEdit_pwd.text()
        login_rember = self.remberme.checkState() # 0就是没有勾

        if login_rember:
            self.rm_type=1
        else:
            self.rm_type=0

        # 对用户输入的状态进行判断
        if self.login_name in self.config.sections():
            # 对现有字段进行设置
            if self.rm_type==1:
                self.config.set_setcion_items(self.login_name,self.login_pwd,self.rm_type)
        else:
            self.config.set_new_section(username=self.login_name,pwd=self.login_pwd,type=self.rm_type)

        # 使用用户账号进行登录

        self.net_thread = NetWorkThread(self.login_name,self.login_pwd)
        self.net_thread._status_signal.connect(self.ntThread_cb) #进行信号连接
        #进行状态检查
        text,status= self.net_thread.first_check()
        if status==False:
            self.qmessage_about(text)
        else:
            self.change_status(True)

            self.showmin()
            self.tray_show_msg("login success,enjoy wonderful time")

            #切换按钮的回调函数
            # 设置其他的槽函数
            self.btn_login.clicked.disconnect(self.onbtn_clicked_login)
            self.btn_login.clicked.connect(self.onbtn_clicked_lougout)
            self.net_thread.start()


    def ntThread_cb(self,msg):
        '''
        登录线程的信号回调函数
        :param str:
        :return:
        '''
        if msg=="W":
            # 网络断开连接
            self.tray_show_msg("login failed,check network adapter status")
            self.net_thread.set_thread_status(True)
        elif msg=="F":
            # 登录错误，可能是账号密码错误
            self.tray_show_msg("login failed,please make sure use correct username or password")
            self.net_thread.set_thread_status(True)
        elif msg=="S":
            self.tray_show_msg("login again success")
        elif msg=="E":
            self.tray_show_msg("logout success!bye")


    def onbtn_clicked_lougout(self,switcher=False):

        if hasattr(self,"net_thread"):
            self.net_thread.set_thread_status(True)
            #text,status =self.net_thread.logout()
            # if not status:
            #     self.qmessage_about(text)
            # else:
            #     self.tray_show_msg(text)
        if not switcher:
            self.change_status(False)

            self.btn_login.clicked.disconnect(self.onbtn_clicked_lougout)
            self.btn_login.clicked.connect(self.onbtn_clicked_login)



    def change_status(self,switcher=False):
        '''
        更改状态
        :return:
        '''
        if switcher==True:

            self.info_label.setText("\rlogin success,have good time!\n\n\rauthor:badao\n\remail:cole_hou@live.com")
            self.info_label.adjustSize() #适应字体大小
            self.info_label.setVisible(True)

            self.lineEdit_name.hide()
            self.lineEdit_pwd.hide()
            self.remberme.hide()
            self.btn_login.setText("Logout")

        else:

            self.info_label.setText("")
            self.info_label.setVisible(False)
            self.lineEdit_name.show()
            self.lineEdit_pwd.show()
            self.lineEdit_name.setText(self.login_name)
            self.lineEdit_pwd.show()
            self.lineEdit_pwd.setText(self.login_pwd)
            self.remberme.show()
            self.btn_login.setText("Login")


    def qmessage_about(self,msg,title="WRONG"):
        return QMessageBox.about(self, title, msg)

    def _addmenu(self):

        restoreAction = QAction("Restore", self,
                                triggered=self.showNormal)

        minAction = QAction("Min", self,
                                triggered=self.showmin)

        quitAction = QAction("&Quit", self,
                             triggered=self.closeOut)

        self.trayIconMenu = QMenu(self)

        self.trayIconMenu.addAction(restoreAction)

        self.trayIconMenu.addAction(minAction)
        self.trayIconMenu.addSeparator()  #加一个分界符
        self.trayIconMenu.addAction(quitAction)

        self.trayIcon = QSystemTrayIcon(self)
        self.trayIcon.setIcon(QIcon(":/logo.ico"))
        self.trayIcon.setContextMenu(self.trayIconMenu)



    def changeEvent(self, event):
        '''
        劫获到状态改变的信息
        :param event:
        :return:
        '''
        if event.type() == QEvent.WindowStateChange:


            # if self.isMinimized():
            #     event.ignore()
            #     self.hide()
            #     self.trayIcon.show()
            #     self.trayIcon.showMessage('МГТУ NetWork Tool', 'Running in the background') #这里可以当作提示信息来进行显示
            #     return


            if self.isMaximized():
                event.ignore()
                self.trayIcon.hide()
                self.show()
                return

    def tray_show_msg(self,msg):
        self.trayIcon.showMessage('МГТУ NetWork Tool', msg)  # 这里可以当作提示信息来进行显示

    def showmin(self):
        '''
        最小化的回掉
        :return:
        '''
        if self.isVisible():
            self.hide()
            self.trayIcon.show()


    def closeOut(self):


        self.onbtn_clicked_lougout(switcher=True)
        self.net_thread.logout()
        if self.trayIcon.isVisible():
            self.trayIcon.hide()

        qApp.quit()

    # 重写鼠标移动窗口事件
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.m_drag = True
            self.m_DragPosition = event.globalPos() - self.pos()
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))

    # 重写鼠标移动窗口事件
    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.m_drag:
            self.move(QMouseEvent.globalPos() - self.m_DragPosition)

            QMouseEvent.accept()

    # 重写鼠标移动窗口事件
    def mouseReleaseEvent(self, QMouseEvent):
        self.m_drag = False
        self.setCursor(QCursor(Qt.ArrowCursor))

    def __some_init(self):
        '''
        设置图标和背景
        :return:
        '''
        palette = QPalette()
        pix = QPixmap(":/bg.jpg")
        pix = pix.scaled(self.width(), self.height())
        palette.setBrush(QPalette.Background, QBrush(pix))
        self.setPalette(palette)

        self.toolButton.setIcon(QIcon(QPixmap(":/logo.ico")))
        self.toolButton.setIconSize(QSize(self.toolButton.geometry().width(),self.toolButton.geometry().height()))



class CheckThread(QThread):
    _signal = pyqtSignal(str)

    def __init__(self, parent=None):
        super(CheckThread, self).__init__()

    def __del__(self):
        self.wait()



if __name__ =="__main__":
    # 自定义分辨率
    QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    app = QApplication(sys.argv)


    md = BMSTU_NT()
    md.show()
    sys.exit(app.exec_())













