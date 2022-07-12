from operator import truediv
import os
import re
import shutil
import sys
import math

import PyQt5
from PyQt5 import (uic , QtCore)
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QAction, QApplication, QFileDialog, QMainWindow,
                             QTextEdit, QMessageBox,QListView,QTreeView,QFileSystemModel,
                             QAbstractItemView,QTableWidget,QTableWidgetItem,
                             QMenu, QInputDialog)


form_class = uic.loadUiType("pyqt.ui")[0]





class WindowClass(QMainWindow, form_class):


    def __init__(self):
        super().__init__()
        
        self.setupUi(self)
 
        self.setWindowTitle("Python GUI Shell")
        self.setWindowIcon(QIcon('logo-python.png'))
 
        self.initUI()
        self.tableItemList = []
        
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

        self.actionsave.triggered.connect(self.save_table_content)
        self.actionload.triggered.connect(self.load_file_content)
     
        self.registerButton.clicked.connect(self.registerNewfile)

        try:
            f = open("fileList.fl","r")
            self.clearAllRow()
            savedFileNum = int(f.readline())
            for row in range(savedFileNum):
                tableWidgetItems = f.readline().split(" ")
                print(tableWidgetItems)
                self.addRow()
                self.updateRow(row,tableWidgetItems)
        except FileNotFoundError:
            print("There is no saved file.")


    def test(self, pos):
        print("KILL me")

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
            self.updateRow(count,fname,fAddress[0],0,0,"Leejihyeon")
            
            #self.tableWidget.resizeColumnsToContents()
            
            print("registerNewfile complete")
        else:
            print("Not select file")
    def updateCell(self,row,col, content):
        self.tableWidget.setItem(row,col,QTableWidgetItem(content))
    def updateRow (self,row,name, address=None, repeatType=None,repeatCycle=None, env=None):
        print(name)
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

        if os.path.exists("fileList.fl") == True:
            os.remove("fileList.fl")
        else:
            pass

        f = open("fileList.fl", 'w')
        
        f.write(str(self.tableWidget.rowCount()))
        f.write("\n")
        for currentRow in range(self.tableWidget.rowCount()):
            print("row num:", self.tableWidget.rowCount())
            for c in range(5):
                item = self.tableWidget.item(currentRow,c).text()
                print("item: ",item)
                f.write(item)
                f.write(" ")
            f.write("\n")
                
        f.close()
        print("완료")
        pass 
    def load_file_content(self):
        try:
            f = open("fileList.fl","r")
            self.clearAllRow()
            savedFileNum = int(f.readline())
            for row in range(savedFileNum):
                tableWidgetItems = f.readline().split(" ")
                print(tableWidgetItems)
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
            self.emptymMenu.addAction("추가", self.addRow)      
            self.emptymMenu.exec_(self.tableWidget.mapToGlobal(pos)) 
            
        # 아이템에서
        else:
            self.menu = QMenu(self)
            self.menu.addAction("실행", lambda: self.fileExecuteWithPos(pos))
            self.menu.addAction("이름 변경", lambda : self.modifyName(pos))
            self.menu.addAction("삭제",lambda: self.deleteRow(pos))      
            self.menu.exec_(self.tableWidget.mapToGlobal(pos)) 

    def modifyName(self, pos):
        print("pos : ", pos)
        print("x, y : ", pos.x(), pos.y())
        targetRow = self.tableWidget.indexAt(pos).row()
        name, ok = QInputDialog.getText(self, 'Input Dialog', 'Enter your name:')    
        if ok == True :
            name_v2 = name.replace(" ", "_")
            self.tableWidget.setItem(targetRow ,0, QTableWidgetItem(name_v2))            
 
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
        targetAddress = self.tableWidget.item(targetRow,1).text().split("/")
        targetFolder = "/".join(targetAddress[0:-1])
        targetfileName = targetAddress[-1]
        targetEnv = self.tableWidget.item(targetRow,4).text()
        print("targetAddress",targetAddress)

        # move target folder
        os.chdir(targetFolder)
        
        extention = targetfileName.split(".")[-1]

        if (extention == "py")     :
            os.system("conda activate "+ targetEnv)
            os.system("python " + targetfileName)
        elif extention == "bat" :
            os.system(targetfileName)
        else:
            os.system(targetfileName)
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()

