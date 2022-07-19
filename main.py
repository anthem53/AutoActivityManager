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
n_dyas_repeat_class = uic.loadUiType('n-days_repeat.ui')[0]
day_repeat_class = uic.loadUiType('dayRepeat.ui')[0]

class dayRepeatDialog(QDialog,day_repeat_class):
    def __init__(self,target=[]):
        super().__init__()

        self.setupUi(self)
        self.initUi()

        if target == []:
            print("default setting")
        else :
            print("existed setting")
    def initUi(self):
        self.okButton.clicked.connect(self.onOKButtonClicked)
        self.cancelButton.clicked.connect(self.onCancelButtonClicked)
    def onOKButtonClicked(self):
        self.accept()
    def onCancelButtonClicked(self):
        self.reject()
    def showModal(self):
        
        isOkclicked = super().exec_()
        selectedDayList = ""

        if self.checkBox_mon.isChecked() == True:
            selectedDayList += "월" 
        if self.checkBox_tues.isChecked() == True:
            selectedDayList += "화"
        if self.checkBox_wed.isChecked() == True:
            selectedDayList += "수"
        if self.checkBox_thur.isChecked() == True:
            selectedDayList += "목"
        if self.checkBox_fri.isChecked() == True:
            selectedDayList += "금"
        if self.checkBox_sat.isChecked() == True:
            selectedDayList += "토"
        if self.checkBox_sun.isChecked() == True:
            selectedDayList += "일"

        return isOkclicked, selectedDayList


class repeatDialog(QDialog,n_dyas_repeat_class):
    def __init__(self):
        super().__init__()
        
        self.setupUi(self)

        self.numberBox.setMaximum(7)
        self.numberBox.setMinimum(1)
        pass
    def showModal(self):

        isOkclicked = super().exec_()
        dayNum = self.numberBox.text()
        dayNum = int(dayNum)
        if dayNum <= 0 :
            dayNum = 0 
        elif dayNum >7 :
            dayNum = 7
        else:
            pass
        return isOkclicked,dayNum



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
        #self.initTimer()

    def initTimer(self):
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.timerFunction)
        self.timer.start()
        self.timerREST = 5

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
        self.actionRepeat_Execute.triggered.connect(self.executeRepeat)

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
    def timerFunction(self):
        if self.timerREST > 0:
            self.timerREST -= 1
            self.logText.setText("%d second rest" % self.timerREST)
        else:
            self.logText.setText("Timer end")
            self.timer.stop()
            #self.fileExecute(4)
            #self.fileExecute(0)

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
            self.updateRow(count,fname,fAddress[0],"반복없음",0,envName)
            
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
    
    def repeatHash(self,text):

        if text == "반복없음":
            return 0 , None
        elif text == "요일마다":
            return 2 , None 
        elif text[1:] == "일마다":
            return 1 , int(text[0])
        else:
            return 3, None

    def dayOfWeekHash(self, dayNum):
        if dayNum == 1 :
            return "월"
        elif dayNum == 2 :
            return "화"
        elif dayNum == 3:
            return "수"
        elif dayNum == 4:
            return "목"
        elif dayNum == 5:
            return "금"
        elif dayNum == 6:
            return "토"
        elif dayNum == 7:
            return "일"
        else :
            return None
    def executeRepeat(self):
        for currentRow in range(self.tableWidget.rowCount()):
            rawRepeatType = self.tableWidget.item(currentRow,2).text()
            repeatType, cycle = self.repeatHash(rawRepeatType)
            if (repeatType == 0):
                print("주기적 실행 파일이 아닙니다.")
                pass
            elif repeatType == 1:
                print("%d일 마다 실행되는 파일입니다." % cycle)
                itemFlag = self.tableWidget.item(currentRow,3).text()
                tempQDate = QDate.fromString(itemFlag, "yyyy MM dd")
                d_day = tempQDate.daysTo(QDate.currentDate()) % 3
                if d_day == 0 :
                    self.fileExecute(currentRow)
                pass
            elif repeatType == 2:
                print("특정 요일마다 실행되는 파일입니다.")
                targetDayofWeek = self.tableWidget.item(currentRow,3).text()
                tempDayofWeek = self.dayOfWeekHash(QDate.currentDate().dayOfWeek())
                print(tempDayofWeek)
                if tempDayofWeek  in targetDayofWeek:
                    self.fileExecute(currentRow)


                pass
            else :
                print("에러 오지게 났음.")
               
        pass
        #while (self.tableWidget.rowCount() > 0):
        #    self.tableWidget.removeRow(0)

    def generateMenu(self, pos):
        # 빈공간에서
        if(self.tableWidget.itemAt(pos) is None):
            pass
        # 아이템에서
        else:
            self.menu = QMenu(self)
            self.menu.addAction("실행", lambda: self.fileExecuteWithPos(pos))
            self.menu.addAction("이름 변경", lambda : self.modifyName(pos))
            self.menu.addSeparator()
            self.menu.addAction("N일 마다 반복 설정", lambda : self.setNdaysRepeat(pos))
            self.menu.addAction("요일 마다 반복 설정",lambda : self.setDayrepeat(pos))
            self.menu.addAction("반복 제거", lambda : self.clearRepeat(pos))
            self.menu.addSeparator()
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
    def clearRepeat(self, pos):
        targetRow = self.tableWidget.indexAt(pos).row()
        self.tableWidget.setItem(targetRow ,2, QTableWidgetItem("반복없음"))            
        self.tableWidget.setItem(targetRow ,3, QTableWidgetItem("0"))                

    def setDayrepeat(self, pos):
        targetRow = self.tableWidget.indexAt(pos).row()
        win = dayRepeatDialog()
        isOkClicked, dayString = win.showModal()
        if isOkClicked == True:
            self.tableWidget.setItem(targetRow ,2, QTableWidgetItem("요일마다"))            
            self.tableWidget.setItem(targetRow ,3, QTableWidgetItem(dayString))                
    def setNdaysRepeat(self, pos):
        targetRow = self.tableWidget.indexAt(pos).row()
        win = repeatDialog()
        isOkClicked,dayNum = win.showModal()
        if isOkClicked:
            print("OK clicked")
            #referenceDate = QDate.currentDate().toString("ddd yyyy MM dd")
            referenceDate = QDate.currentDate().toString("yyyy MM dd")
            self.tableWidget.setItem(targetRow ,2, QTableWidgetItem("%s일마다" % str(dayNum)))            
            self.tableWidget.setItem(targetRow ,3, QTableWidgetItem(referenceDate))                

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
            #os.remove(targetFolderForBatch+"\\tempBatch.bat")
            print("targetFolderForBatch", targetFolderForBatch)
            print()
        else:
            os.system(targetAddressForBatch)

    def convert2BatchAddress (self,address):
        addressItemList = address.split("/")
        resultList = []

        for e in addressItemList:
            if ' ' in e :
                resultList.append("\""+e+"\"")
            else:
                resultList.append(e)
        result = '/'.join(resultList)
        return result

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





if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()

