import time, sys
from threading import Thread

from PySide2 import QtCore

from PySide2.QtWidgets import *
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import Signal,QObject

from qt_material import apply_stylesheet

import numpy as np
import pandas as pd

from GPS_API import GPS_API

#+++创建信号类+++
class mySignal(QObject):
    
    result = Signal(QPlainTextEdit, str)
    progress_update = Signal(int)
    information = Signal(QWidget, str)
    
#+++创建界面类+++    
class GPSMainWindow:
    def __init__(self):
        
        #加载界面
        self.ui = QUiLoader().load('gps.ui')
        #self.ui.buttonGroup1.buttonClicked.connect(self.ButtonGroup1Clicked)
        
        #设置 radio default 值
        self.ui.tencent_rd_1.setChecked(True)
        self.ui.tencent_rd_2.setChecked(True)
        self.ui.tencent_rd_3.setChecked(True)
        
        #关联按键功能
        self.ui.Submit1.clicked.connect(self.Submit1Thread)
        self.ui.Submit2.clicked.connect(self.Submit2Thread)
        self.ui.Submit3.clicked.connect(self.Submit3Thread)
        self.ui.ClearButton.clicked.connect(self.ClearDisplay)
        
        self.ui.OpenFileButton.clicked.connect(self.OpenFileClick)
        
        #实例化信号类
        self.ms = mySignal()
        #连接信号内容接受函数+++++
        self.ms.result.connect(self.messagePrint1)
        self.ms.progress_update.connect(self.setProgress)
        self.ms.information.connect(self.ShowWarning2)
        
        #实例化API类
        self.gps_api = GPS_API()
   
    def Submit1(self, address, rd):
        
        #time.sleep(2)
        if rd == '腾讯':
            gps1 = self.gps_api.addressToLocationbyTENCENT(address)
        elif rd == '百度':
            gps1 = self.gps_api.addressToLocationbyBaidu(address)
        elif rd == '高德':
            gps1 = self.gps_api.addressToLocationbyAmap(address)
        
        #信号内容发送函数
        self.ms.result.emit(self.ui.Text2, rd+": ")
        self.ms.result.emit(self.ui.Text2, gps1)
        #self.ms.result.emit(self.ui.Text2, "\n")
    
    def Submit2(self, long, lat, rd):
        
        location = long + ',' + lat
        #time.sleep(2)
        if rd == '腾讯':
            address2 = self.gps_api.locationToAddressbyTENCENT(location)
        elif rd == '百度':
            address2 = self.gps_api.locationToAddressbyBaidu(location)
        elif rd == '高德':
            address2 = self.gps_api.locationToAddressbyAmap(location)
        
        #信号内容发送+++++
        self.ms.result.emit(self.ui.Text2, rd+": ")
        self.ms.result.emit(self.ui.Text2, address2)
        #self.ms.result.emit(self.ui.Text2, "\n")
        
    def Submit3(self, fname, rd):
        
        self.ui.Submit3.setEnabled(False)
        address_raw_data = pd.read_excel(io=(fname), sheet_name=0, header=0)
        address_raw_data = address_raw_data.loc[:, ['名称', '地址']]
        address_data = address_raw_data.dropna(axis=0, how='all', subset=["地址"])
        address_data['经纬度'] = np.nan
        
        len_of_address = len(address_data)
        for x in range(len_of_address):
            if rd == '腾讯':
                address_data.iloc[x, 2] = self.gps_api.addressToLocationbyTENCENT(address_data.iloc[x, 1])
            elif rd == '百度':
                address_data.iloc[x, 2] = self.gps_api.addressToLocationbyBaidu(address_data.iloc[x, 1])
            elif rd == '高德':
                address_data.iloc[x, 2] = self.gps_api.addressToLocationbyAmap(address_data.iloc[x, 1])
            
            #self.ms.result.emit(self.ui.Text2, rd+": ")
            self.ms.result.emit(self.ui.Text2, address_data.iloc[x, 1]+","+address_data.iloc[x, 2])
            self.ms.progress_update.emit(int((x+1)/len_of_address*100))
         
        if self.ui.ExportFile.isChecked():
            writer = pd.ExcelWriter('./经纬度.xlsx')
            address_data.to_excel(writer, index=True, sheet_name='GPS')
            writer.save()
            #self.ms.result.emit(self.ui.Text2, '++++++批量转换完成，数据已导出！++++++')
            self.ms.information.emit(self.ui, '++++++批量转换完成，数据已导出！++++++')
        else:
            #self.ms.result.emit(self.ui.Text2, '++++++批量转换完成！++++++')
            self.ms.information.emit(self.ui, '++++++批量转换完成！++++++')
        
        self.ui.Submit3.setEnabled(True)
    
    def Submit1Thread(self):
        address1 = self.ui.Address.text()
        rd1 = self.ui.buttonGroup1.checkedButton().text()
        
        #创建子线程，io操作在子线程中完成
        if len(address1) > 0:
            thread = Thread(target=self.Submit1,args=(address1, rd1))
            thread.start()
        else:
            self.ShowWarning("请输入正确地址！")
            
    def Submit2Thread(self):
        long = self.ui.LongText.text()
        lat = self.ui.LatText.text()
        rd2 = self.ui.buttonGroup2.checkedButton().text()
        
        if len(long) > 0 and len(lat) > 0:
            thread = Thread(target=self.Submit2,args=(long, lat, rd2))
            thread.start()
        else:
            self.ShowWarning("请输入正确经纬度！")
            
    def Submit3Thread(self):
        fname = self.ui.FileLabel.text()
        #print(fname)
        rd3 = self.ui.buttonGroup3.checkedButton().text()
        
        if len(fname) > 0:
            thread = Thread(target=self.Submit3,args=(fname, rd3))
            thread.start()
        else:
            self.ShowWarning("请选择批量转换文件！")
    
    def OpenFileClick(self):
        fname = self.OpenFile()
        print(fname)
        filename = fname
        fileNameLen = -1 * (len(filename) - filename.rfind('/')) + 1
        filename = filename[fileNameLen:]
        self.ui.FileLabel.setText(filename)
        
    def OpenFile(self):
        fname = QFileDialog.getOpenFileName(self.ui, 'Open file', './',"excel(*.xlsx *.xls)")
        #askopenfilename(title='文件选择', initialdir='./', filetypes=[('excel', ['.xls', '.xlsx'])])
        filename = fname[0]
        #fileNameLen = -1 * (len(filename) - filename.rfind('/')) + 1
        #filename = filename[fileNameLen:]
        return filename
    
    def ClearDisplay(self):
        self.ui.Text2.clear()
        self.ui.progressBar.setValue(0)
        
    def ShowWarning(self, str):
        messageBox = QMessageBox()
        messageBox.information(self.ui, "Warning", str)
    
    #信号接受函数+++++
    @QtCore.Slot(QObject, str)
    def messagePrint1(self, Text, str):
        #Text.textCursor().insertText(str)
        Text.append(str)
        
    @QtCore.Slot(int)
    def setProgress(self, value):
        self.ui.progressBar.setValue(value)
    
    @QtCore.Slot(QWidget, str)
    def ShowWarning2(self, ui, str):
        messageBox = QMessageBox()
        messageBox.information(ui, "Warning", str)
        
    """
    def ButtonGroup1Clicked(self):
        rd = self.ui.buttonGroup1.checkedButton().text()
        print(rd)
        return rd
    """
        
if __name__ == '__main__':
    if not QApplication.instance():
        app = QApplication()
    else:
        app = QApplication.instance()
    
    apply_stylesheet(app, theme='dark_cyan.xml')
    
    myApp = GPSMainWindow()
    myApp.ui.show()

    app.exec_()
