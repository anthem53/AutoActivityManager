import os
import sys
import webbrowser
import math, re, shutil

import PyQt5
from PyQt5 import (uic , QtCore)
from PyQt5.QtGui import * 
from PyQt5.QtWidgets import * 
from PyQt5.QtCore import *

form_class = uic.loadUiType("pyqt.ui")[0]

class WindowClass(QMainWindow, form_class):


    def __init__(self):
        super().__init__()
        
        self.setupUi(self)
 
        self.setWindowTitle("Python GUI Shell")
        self.setWindowIcon(QIcon('logo-python.png'))
 
        self.thisFileAddress = os.path.realpath(__file__)
        tempList = self.thisFileAddress.split("\\")
        self.saveDirectory = "/".join(tempList[0:-1])

        self.initUI()
        self.initTraySystem()
        self.initTimer()

    def initTimer(self):
        self.timer = QTimer()
    
    def initTraySystem(self):
        trayIcon = QIcon("logo-python.png")
        self.trayElement = QSystemTrayIcon(self)
        self.trayElement.setIcon(trayIcon)
        show_action = QAction("Show", self)
        quit_action = QAction("Exit", self)
        hide_action = QAction("Hide", self)
        show_action.triggered.connect(self.show)
        hide_action.triggered.connect(self.hide)
        quit_action.triggered.connect(qApp.quit)
        tray_menu = QMenu()
        tray_menu.addAction(show_action)
        tray_menu.addAction(hide_action)
        tray_menu.addAction(quit_action)
        self.trayElement.setContextMenu(tray_menu)
        self.trayElement.show()
 
    def initUI(self):

        self.tableWidget.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        self.tableWidget.setSizeAdjustPolicy(PyQt5.QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.tableWidget.setColumnWidth(0,int(self.width() * 0.3))
        self.tableWidget.setColumnWidth(1,int(self.width() * 0.4))
        self.tableWidget.setColumnWidth(2,int(self.width() * 0.1))
        self.tableWidget.setColumnWidth(3,int(self.width() * 0.1))
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.customContextMenuRequested.connect(self.generateMenu)
        self.tableWidget.doubleClicked.connect(self.tableWidget_doubleClicked)

        self.actionadd_file.triggered.connect(self.registerNewfile)
        self.actionsave.triggered.connect(self.save_table_content)
        self.actionload.triggered.connect(self.load_file_content)
        self.actionShow_current_time.triggered.connect(self.test)
     
        self.registerButton.clicked.connect(self.registerNewfile)

        try:
            f = open("fileList.fl","r")
            self.clearAllRow()
            savedFileNum = int(f.readline())
            for row in range(savedFileNum):
                tableWidgetItems = f.readline().split("   ")
                #print(tableWidgetItems)
                self.addRow()
                self.updateRow(row,tableWidgetItems)
        except FileNotFoundError:
            print("There is no saved file.")


    def test(self):
        print("KILL me")
        self.logText.setText(QDateTime.currentDateTime().toString("ddd.h.m.s"))

    def registerNewfile(self):
        
        # file dialog 
        fAddress = QFileDialog.getOpenFileName(self, 'Open file', './')
        
        if (fAddress[0] != ""):
            count  = self.tableWidget.rowCount()
            self.addRow()
            fNames = fAddress[0].split("/") 
            fname = fNames[-2] + "/" + fNames[-1] 
            print("self.tableWidget.rowCount(): ", self.tableWidget.rowCount())
            firstColumn = 0

            envName, ok = QInputDialog.getText(self, 'Input Dialog', 'Enter new Env Name:')    
            if ok != True :
                envName = "Leejihyeon" 
            self.updateRow(count,fname,fAddress[0],0,0,envName)
            
            #self.tableWidget.resizeColumnsToContents()
            
            print("registerNewfile complete")
        else:
            print("Not select file")

    def updateCell(self,row,col, content):
        self.tableWidget.setItem(row,col,QTableWidgetItem(content))
    def updateRow (self,row,name, address=None, repeatType=None,repeatCycle=None, env=None):
        #print(name)
        if type(name)== str:
            firstColumn = 0
            repeatType = str(repeatType)
            repeatCycle = str(repeatCycle)
            self.tableWidget.setItem(row ,firstColumn, QTableWidgetItem(name))
            self.tableWidget.setItem(row  ,firstColumn + 1, QTableWidgetItem(address))
            self.tableWidget.setItem(row  ,firstColumn + 2, QTableWidgetItem(repeatType))
            self.tableWidget.setItem(row  ,firstColumn + 3, QTableWidgetItem(repeatCycle))
            self.tableWidget.setItem(row  ,firstColumn + 4, QTableWidgetItem(env))
        elif type(name) == list:
            itemList = name
            for col,e in enumerate(itemList):
                if type(e) != str:
                    e = str(e)
                else:
                    pass
                self.updateCell(row,col,e)
        else:
            pass
        pass

    def save_table_content(self):

        savedfile  = self.saveDirectory + "/fileList.fl"
        print(savedfile)
        if os.path.exists(savedfile) == True:
            os.remove(savedfile)
        else:
            pass

        f = open(savedfile, 'w')
        
        f.write(str(self.tableWidget.rowCount()))
        f.write("\n")
        for currentRow in range(self.tableWidget.rowCount()):
            for c in range(5):
                item = self.tableWidget.item(currentRow,c).text()
                #print("item: ",item)
                f.write(item)
                f.write("   ")
            f.write("\n")
                
        f.close()
        self.logText.setText("저장 완료")
        pass 
    def load_file_content(self):
        try:
            savedfile = self.saveDirectory +  "fileList.fl"
            f = open(savedfile,"r")
            self.clearAllRow()
            savedFileNum = int(f.readline())
            for row in range(savedFileNum):
                tableWidgetItems = f.readline().split("   ")
                #print(tableWidgetItems)
                self.addRow()
                self.updateRow(row,tableWidgetItems)
        except FileNotFoundError:
            print("There is no saved file.")
    def tableWidget_doubleClicked(self):
        row = self.tableWidget.currentIndex().row()
        self.fileExecute(row)
        
        print("double click execute")
    def addRow(self):
        # 마지막줄에 추가하기 위함
        rowPosition =self.tableWidget.rowCount()
        self.tableWidget.insertRow(rowPosition)
    
    def generateMenu(self, pos):
        # 빈공간에서
        if(self.tableWidget.itemAt(pos) is None):
            self.emptymMenu = QMenu(self)
            #self.emptymMenu.addAction("추가", self.addRow)      
            self.emptymMenu.exec_(self.tableWidget.mapToGlobal(pos)) 
            
        # 아이템에서
        else:
            self.menu = QMenu(self)
            self.menu.addAction("실행", lambda: self.fileExecuteWithPos(pos))
            self.menu.addAction("이름 변경", lambda : self.modifyName(pos))
            self.menu.addAction("가상환경 변경", lambda : self.modifyEnv(pos))
            self.menu.addAction("해당 폴더 열기",lambda : self.openTargetFileFolder(pos))
            self.menu.addAction("삭제",lambda: self.deleteRow(pos))      
            self.menu.exec_(self.tableWidget.mapToGlobal(pos)) 

    def openTargetFileFolder (self,pos):
        targetRow = self.tableWidget.indexAt(pos).row()
        targetAddress = self.tableWidget.item(targetRow,1).text()
        targetAddressList = targetAddress.split("/")
        targetFolder = "/".join(targetAddressList[0:-1])
        webbrowser.open("\"%s\"" % targetFolder)
    def modifyName(self, pos):
       
        targetRow = self.tableWidget.indexAt(pos).row()
        name, ok = QInputDialog.getText(self, 'Input Dialog', 'Enter your name:')    
        if ok == True :
            name_v2 = name.replace(" ", "_")
            self.tableWidget.setItem(targetRow ,0, QTableWidgetItem(name_v2))            
    def modifyEnv(self, pos):
        targetRow = self.tableWidget.indexAt(pos).row()
        name, ok = QInputDialog.getText(self, 'Input Dialog', 'Enter new Env Name:')    
        if ok == True :
            name_v2 = name.replace(" ", "_")
            self.tableWidget.setItem(targetRow ,4, QTableWidgetItem(name_v2))            
    
    def deleteRow (self, pos):
        print("call DeleteRow")
        self.tableWidget.removeRow(self.tableWidget.indexAt(pos).row())
    
    def clearAllRow(self):
        while (self.tableWidget.rowCount() > 0):
            self.tableWidget.removeRow(0)
        
    def fileExecuteWithPos(self,pos):
        targetRow = self.tableWidget.indexAt(pos).row()
        self.fileExecute(targetRow)

    def fileExecute(self, targetRow):
        # Parsing part
        targetAddress = self.tableWidget.item(targetRow,1).text()
        targetAddressList = targetAddress.split("/")
        targetFolder = "/".join(targetAddressList[0:-1])
        targetfileName = targetAddressList[-1]
        targetEnv = self.tableWidget.item(targetRow,4).text()
        #print("targetAddressList",targetAddressList)
        #print("targetAddress",targetAddress)
        # move target folder
        os.chdir(targetFolder)
        
        extention = targetfileName.split(".")[-1]
        targetFolderForBatch = self.convert2BatchAddress(targetFolder)
        targetAddressForBatch = self.convert2BatchAddress(targetAddress)

        if (extention == "py")     :

            with open(targetFolder+"/tempBatch.bat","w") as pythonBatch:
                pythonBatch.write("cd %s \n" % targetFolderForBatch )
                pythonBatch.write("call conda activate "+targetEnv +"\n")
                pythonBatch.write("python " + targetAddressForBatch+"\n")
                pythonBatch.write("call conda deactivate\n")

            os.system(targetFolderForBatch+"/tempBatch.bat")
            os.remove(targetFolderForBatch+"/tempBatch.bat")
        elif extention == "bat" :
            #os.system(targetfileName)
            os.system(targetAddressForBatch)
        elif extention == "exe":
            with open(targetFolder+"/tempBatch.bat","w") as exeBatch :
                exeBatch.write("start "+""+targetAddressForBatch+"\n")

            os.system(targetFolderForBatch+"/tempBatch.bat")
            #os.remove(targetFolder+"/tempBatch.bat")
        else:
            os.system(targetAddressForBatch)
    def writeBatch(self,f_opend,address):
        convertedAddress = self.convert2BatchAddress(address)
        f_opend.write(convertedAddress)
    def convert2BatchAddress (self,address):
        addressItemList = address.split("/")
        resultList = []

        for e in addressItemList:
            if ' ' in e :
                resultList.append("\""+e+"\"")
            else:
                resultList.append(e)
        result = '\\'.join(resultList)
        return result
    def writeBatchFile(self,batchfile,address):
        batchfile.write(self.convert2BatchAddress(address))

    def closeEvent(self, event):

        saved = QMessageBox.question(self, 'Message', 'Do you want to SAVE?',
                            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if saved == QMessageBox.Yes:
            self.save_table_content()
        else:
            pass

        reply = QMessageBox.question(self, 'Message', 'Are you sure to QUIT?\nIf not, the program is on the TRAY.',
                            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
            self.hide()
            self.trayElement.showMessage(
                "Tray Program",
                "Application was minimized to Tray",
                QSystemTrayIcon.Information,
                2000
            )

class timer :
    def __init__(self):
        self.test = None




if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()

