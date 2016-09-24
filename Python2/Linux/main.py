#!/usr/bin/python
#-*- coding:utf-8 -*-

import codecs
import sys
import os
import subprocess
from PyQt4 import QtGui, QtCore, Qt
from dialog import DelDialog
from aboutDialog import aboutDialog

fileSupported = ['bat', 'css', 'doc', 'docx', 'exe', 'iso', 'jpg', 'mp3', 'pdf', 'png' ,'ppt', 'pptx', 'py', 'rar', 'txt', 'zip']

class mainWin(QtGui.QWidget):
    def __init__(self):
        super(mainWin, self).__init__()
        self.setWindowTitle(u'光速启动')
        self.setWindowIcon(QtGui.QIcon('./images/light_speed.png'))
        self.initMain()
        self.createContextMenu()
        self.resize(150, 300)

        self.icon = QtGui.QSystemTrayIcon()
        self.icon.setIcon(QtGui.QIcon('./images/light_speed.png'))
        self.initIcon()

        screen = QtGui.QDesktopWidget().screenGeometry()
        self.wid = screen.width()
        self.hei = screen.height()

        self.setAcceptDrops(True)

    def initMain(self):
        self.btnList = []
        try:
            self.grid = QtGui.QGridLayout()
            with codecs.open('./data/main.txt', 'r', 'utf-8') as f:
                res = f.read().splitlines()
                self.cnt = 0
                for line in res:
                    self.createPushButton(line, res.index(line))
            self.setLayout(self.grid)
            with open('./style/main.css', 'r') as f:
                self.setStyleSheet(f.read())
        except IOError:
            pass

    def initIcon(self):
        self.icon.showAction = QtGui.QAction(u"&显示窗口", self, triggered = self.showMain)
        self.icon.quitAction = QtGui.QAction(u"&退出", self, triggered = sys.exit)
        
        self.icon.trayIconMenu = QtGui.QMenu()
        self.icon.trayIconMenu.addAction(self.icon.showAction)
        self.icon.trayIconMenu.addAction(self.icon.quitAction)
        self.icon.setContextMenu(self.icon.trayIconMenu)

    def closeEvent(self, event):
        self.hide()
        self.icon.show()
        event.ignore()

    def showMain(self):
        self.icon.hide()
        self.show()

    def enterEvent(self, event):
        self.right = self.x() + self.width()
        if self.right >= self.wid:
            self.setGeometry(self.wid - self.width(), 30, 150, self.hei)
    
    def leaveEvent(self, event):
        self.right = self.x() + self.frameGeometry().width()
        if self.right >= self.wid:
            self.setGeometry(self.wid + 233, 30, 150, self.hei)

    def mousePressEvent(self, event):
        if event.buttons() == Qt.Qt.LeftButton:
            self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.Qt.LeftButton:
            self.move(event.globalPos() - self.dragPosition)
            event.accept()

    def findBtn(self, btn):
        for listBtn in self.btnList:
            if(btn == listBtn[0]):
                return listBtn[1]

    def react(self):
        sender = self.sender()
        subprocess.call(["xdg-open", self.findBtn(sender)])

    def createContextMenu(self):
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showContextMenu)
        self.contextMenu = QtGui.QMenu(self)
        self.aFile = self.contextMenu.addAction(u'添加文件')
        self.aDir = self.contextMenu.addAction(u'添加文件夹')
        self.delete = self.contextMenu.addAction(u'删除')
        self.aboutAct = self.contextMenu.addAction(u"关于")
        self.clo = self.contextMenu.addAction(u'关闭窗口')

        self.aFile.triggered.connect(self.addFile)
        self.aDir.triggered.connect(self.addDir)
        self.delete.triggered.connect(self.delItem)
        self.clo.triggered.connect(self.close)
        self.aboutAct.triggered.connect(self.about)

    def about(self):
        aboutDialog().exec_()

    def showContextMenu(self, pos):
        self.contextMenu.move(self.pos() + pos)
        self.contextMenu.show()
    
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                line = str(url.toLocalFile())
                line = line.replace('\\','/')
                with codecs.open('./data/main.txt', 'r+', 'utf-8') as f:
                    res = f.read()
                    if line in res.splitlines():
                        return
                    if res == '':
                        pass
                    else:
                        f.write('\n')
                    f.write(line)
                with codecs.open('./data/main.txt', 'r', 'utf-8') as f:
                    lineNum = len(f.read().splitlines()) - 1
                self.createPushButton(line, lineNum)
            event.acceptProposedAction()
    
    def addFile(self):
        line = str(QtGui.QFileDialog.getOpenFileName())
        line = line.replace('\\','/')
        with open('./data/main.txt', 'r+', encoding = 'utf-8') as f:
            res = f.read()
            if line in res.splitlines():
                return
            if res == '':
                pass    
            else:
                f.write('\n')
            f.write(line)
        with open('./data/main.txt', 'r', encoding = 'utf-8') as f:
            lineNum = len(f.read().splitlines()) - 1
        self.createPushButton(line, lineNum)

    def addDir(self):
        line = str(QtGui.QFileDialog.getExistingDirectory())
        line = line.replace('\\','/')
        with open('./data/main.txt', 'r+', encoding = 'utf-8') as f:
            res = f.read()
            if line in res.splitlines():
                return
            if res == '':
                pass
            else:
                f.write('\n')
            f.write(line)
        with open('./data/main.txt', 'r', encoding = 'utf-8') as f:
            lineNum = len(f.read().splitlines()) - 1
        self.createPushButton(line, lineNum)

    def createPushButton(self, line, lineNum):
        btn = QtGui.QPushButton(line.split('/')[-1])
        suffix = line.split('.')
        if os.path.isdir(line):
            btn.setProperty('dir', 'true')
        elif suffix[-1] not in fileSupported:
            btn.setProperty('unknown', 'true')
        else:
            btn.setProperty(suffix[-1], 'true')
        self.btnList.append([btn, line])
        self.connect(btn, QtCore.SIGNAL('clicked()'), self.react)
        self.grid.addWidget(btn, lineNum/3 , self.cnt, 1, 1)
        self.cnt = (self.cnt + 1) % 3
                    
    def delItem(self):
        with open('./data/main.txt', 'r', encoding = 'utf-8') as f:
            res = f.read().splitlines()
        DelDialog(u'删除', res).exec_()
        for item in self.btnList:
            item[0].setParent(None)
            self.grid.removeWidget(item[0])
        with open('./data/main.txt', 'r', encoding = 'utf-8') as f:
            res = f.read().splitlines()
            self.cnt = 0
            self.btnList = []
            for line in res:
                self.createPushButton(line, res.index(line))

os.chdir('/root/learning/learnPython/gsqd4linux')
app = QtGui.QApplication(sys.argv)
ex = mainWin()
ex.show()
app.exec_()
