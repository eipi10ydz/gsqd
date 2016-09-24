#-*- coding:utf-8 -*-

import sys
from PyQt4 import QtGui, QtCore

class aboutDialog(QtGui.QDialog):
    def __init__(self):
        super(aboutDialog, self).__init__()
        self.about()

    def about(self):
        self.setWindowTitle("关于")
        self.setWindowIcon(QtGui.QIcon('./images/light_speed.png'))
        layout = QtGui.QVBoxLayout()
        labelArthur = QtGui.QLabel('作者:eipi10')
        labelEmail = QtGui.QLabel('邮箱:gdzjydz AT mail.ustc.edu.cn')
        labelText = QtGui.QLabel('有什么意见建议，欢迎发邮件向我吐槽!')
        self.okButton = QtGui.QPushButton('ok')

        layout.addWidget(labelArthur)
        layout.addWidget(labelEmail)
        layout.addWidget(labelText)
        layout.addWidget(self.okButton)
        self.connect(self.okButton, QtCore.SIGNAL('clicked()'), self.reactAbout)
        self.setLayout(layout)

    def reactAbout(self):
        sender = self.sender()
        if sender == self.okButton:
            self.close()