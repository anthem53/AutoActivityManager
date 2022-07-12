from operator import truediv
import os
import re
import shutil
import sys
import math

import PyQt5
from PyQt5 import (uic , QtCore)
from PyQt5.QtWidgets import (QAction, QApplication, QFileDialog, QMainWindow,
                             QTextEdit, QMessageBox,QListView,QTreeView,QFileSystemModel,
                             QAbstractItemView,QTableWidget,QTableWidgetItem,
                             QMenu)


form_class = uic.loadUiType("pyqt.ui")[0]





class WindowClass(QMainWindow, form_class):
    class widgetItem ():
        def __init__(self,name = None, address = None, repeatType = None, repeatCycle = None):
            self.name = None
            self.address = None
            self.repeatType = 0
            self.repeatCycle = 0

        def setItemContent(self,name = None, address = None, repeatType = None, repeatCycle = None):
            if name != None :
                self.name = name
            if address != None : 
                self.address = address
            if repeatType != None:
                self.repeatType = repeatType
            if repeatCycle != None:
                self.repeatCycle = repeatCycle

        def getItemContent(self):
            return (self.name,self.address,self.repeatType,self.repeatCycle)
            

    def __init__(self):
        super().__init__()
        
        self.setupUi(self)
        self.initUI()
        self.tableItemList = []
        
    def initUI(self):

        self.tableWidget.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        self.tableWidget.setSizeAdjustPolicy(PyQt5.QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.tableWidget.setColumnWidth(0,int(self.width() * 0.3))
        self.tableWidget.setColumnWidth(1,int(self.width() * 0.4))
        self.tableWidget.setColumnWidth(2,int(self.width() * 0.1))
        self.tableWidget.setColumnWidth(3,int(self.width() * 0.1))

        self.tableWidget.customContextMenuRequested.connect(self.generateMenu)


        self.registerButton.clicked.connect(self.registerNewfile)



    def test(self, pos):
        print("KILL me")

    def registerNewfile(self):
        
        # file dialog 
        fAddress = QFileDialog.getOpenFileName(self, 'Open file', './')
        
        if (fAddress[0] != ""):
            self.addRow()
            fNames = fAddress[0].split("/") 
            fname = fNames[-2] + "/" + fNames[-1] 
            count  = len(self.tableItemList)
            firstColumn = 0
            secondColumn = firstColumn + 1
            thirdColumn = secondColumn + 1
            forthColume = thirdColumn + 1
            self.tableWidget.setItem(count ,firstColumn, QTableWidgetItem(fname))
            self.tableWidget.setItem(count  ,secondColumn, QTableWidgetItem(fAddress[0]))
            self.tableWidget.setItem(count  ,thirdColumn, QTableWidgetItem(str(0)))
            self.tableWidget.setItem(count  ,forthColume, QTableWidgetItem(str(0)))

            self.tableItemList.append(self.widgetItem(fname, fAddress, 0,0))
            #self.tableWidget.resizeColumnsToContents()
            
            print("registerNewfile complete")
        else:
            print("Fail")

        
        # 주소
        pass
        
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
            self.menu.addAction("실행", lambda: self.fileExecute(pos))
            self.menu.addAction("삭제",lambda: self.deleteRow(pos))      
            self.menu.exec_(self.tableWidget.mapToGlobal(pos)) 

        
    def deleteRow (self, pos):
        print("call DeleteRow")
        self.tableWidget.removeRow(self.tableWidget.indexAt(pos).row())
    
    def fileExecute(self, pos):
        targetRow = self.tableWidget.indexAt(pos).row()
        targetAddress = self.tableWidget.item(targetRow,1).text().split("/")
        targetFolder = "/".join(targetAddress[0:-1])
        targetfileName = targetAddress[-1]
        print("targetAddress",targetAddress)
        os.chdir(targetFolder)
        os.system("python " + targetfileName)
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()

