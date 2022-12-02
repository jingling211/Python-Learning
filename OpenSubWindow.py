import time, sys
import requests
import urllib3
import re

from threading import Thread

from PySide2 import QtCore
from PySide2.QtWidgets import *
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import Signal,QObject

from qt_material import apply_stylesheet

urllib3.disable_warnings()

#+++创建信号类+++
class mySignal(QObject):
    
    OutputSig = Signal(str)
    #progress_update = Signal(int)
    #information = Signal(QWidget, str)
    
class PostManWindow:
    def __init__(self):
        
        #加载界面
        self.ui = QUiLoader().load('postman.ui')
        self.ui.Add.clicked.connect(self.add_reqeust_header)
        self.ui.Minus.clicked.connect(self.del_request_header)
        self.ui.Submit.clicked.connect(self.sendReqeustThread)
        
        #实例化信号类
        self.ms = mySignal()
        #连接信号内容接受函数+++++
        self.ms.OutputSig.connect(self.print_response)
    
    def add_reqeust_header(self):
        self.ui.KeyValue.insertRow(0) 
        
    def del_request_header(self):
        self.ui.KeyValue.removeRow(0)
        
    #def pretty_print_response(self, content):
    #    self.ui.Output.appendPlainText(content.decode('GB2312'))

    def ShowWarning(self, str):
        messageBox = QMessageBox()
        messageBox.information(self.ui, "Warning", str)
        
    def sendReqeustThread(self):
        URL = self.ui.URL.text()
        # match URL
        matched = re.match(r'[a-zA-Z]+://[^\s]*[.com|.cn|.net|.org|.edu]', URL, re.I)
        
        #创建子线程，io操作在子线程中完成
        if matched:
            thread = Thread(target=self.sendRequest)
            thread.start()
        else:
            self.ShowWarning("请输入正确地址！")
        
    def sendRequest(self):

        method = self.ui.Method.currentText()
        url    = self.ui.URL.text()
        payload = self.ui.InputString.toPlainText()

        # 获取消息头
        headers = {}
        # 此处省略一些对消息头的处理

        req = requests.request(method, url, headers=headers, data=payload, verify=False)

        #prepared = req.prepare()
        #print(prepared)
        #self.pretty_print_request(prepared)
        #s = requests.Session()
        
        try:
            # 发送请求并且接收响应消息
            #r = s.send(prepared)
            # 打印出响应消息
            self.ms.OutputSig.emit(req.content.decode(req.apparent_encoding))
        except:
            self.ui.Output.appendPlainText(
                traceback.format_exc())
        
        
    @QtCore.Slot(QObject, str)   
    def print_response(self, str):
        self.ui.Output.setPlainText(str)
    
        
class LoginWindow():
    def __init__(self):
        super().__init__()
        #self.setWindowTitle('Login')

        #加载界面
        self.ui = QUiLoader().load('login.ui')
        self.ui.Login.clicked.connect(self.LoginValidation)
        
    def LoginValidation(self):
        UserID = self.ui.UserID.text()
        Password = self.ui.Password.text()
        if len(UserID) > 0 or len(Password) > 0:
            if UserID == "admin" and Password == "123456":
                self.open_new_window()
            else:
                self.ShowWarning("请输入正确账号密码！")
        else:
            self.ShowWarning("请输入账号密码！")

    def open_new_window(self):
        # 实例化另外一个窗口
        self.PostManWindow = PostManWindow()
        # 显示新窗口
        self.PostManWindow.ui.show()
        # 关闭自己
        self.ui.close()

    def ShowWarning(self, str):
        messageBox = QMessageBox()
        messageBox.information(self.ui, "Warning", str)
        
if __name__ == '__main__':
    if not QApplication.instance():
        app = QApplication()
    else:
        app = QApplication.instance()
    
    apply_stylesheet(app, theme='dark_cyan.xml')
    
    myApp = LoginWindow()
    myApp.ui.show()

    app.exec_()
