from threading import Thread

from PySide2 import QtCore
from PySide2.QtWidgets import *
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import Signal,QObject


#template for sub window, multi thread, signal applications

#+++创建信号类+++
class mySignal(QObject):
    
    #定义信号变量，信号接受类型 int， str， object
    Signal1 = Signal(str)

class SubWindow:
    #初始化
    def __init__(self):
        #加载界面
        self.ui = QUiLoader().load('subwindow.ui')
        #链接操作函数（线程操作函数）
        #非阻塞操作可以直接调用普通函数，阻塞操作可以调用线程操作函数
        self.ui.action_item.clicked.connect(self.actionTread)
    
    #定义操作内容    
    def action(self):
        #信号发送函数
        self.ms.Signal1.emit(str)
     
    #使用线程函数调用操作
    def actionThread(self):
        thread = Thread(target=self.action,args=(arg1, arg2))
        thread.start()
        
    #信号接受函数+++++
    @QtCore.Slot(QObject, str)
    def messagePrint1(self, str):
        #Text.textCursor().insertText(str)
        self.ui.Text.append(str)
    
        
class MainWindow:
    def __init__(self):
        super().__init__()

        #加载界面
        self.ui = QUiLoader().load('login.ui')
    
    #打开新窗口函数
    def open_new_window(self):
        # 实例化另外一个窗口
        self.PostManWindow = PostManWindow()
        # 显示新窗口
        self.PostManWindow.ui.show()
        # 关闭自己
        self.ui.close()
        
if __name__ == '__main__':
    if not QApplication.instance():
        app = QApplication()
    else:
        app = QApplication.instance()
    
    #apply_stylesheet(app, theme='dark_cyan.xml')
    
    myApp = MainWindow()
    myApp.ui.show()

    app.exec_()
