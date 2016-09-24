#-*- coding:utf-8 -*-

import codecs
import sys
from PyQt4 import QtGui, QtCore

class DelDialog(QtGui.QDialog):
	def __init__(self, text = '', options = []):
		super(DelDialog, self).__init__()
		self.setWindowTitle(text)
		self.options = options
		self.short = []
		self.initDialog()

	def initDialog(self):
		grid = QtGui.QGridLayout()
		self.combo = QtGui.QComboBox()
		for item in self.options:
			self.short.append(item.split('/')[-1])
			self.combo.addItem(item.split('/')[-1])
		grid.addWidget(self.combo, 0, 0, 1, 2)
		self.okBtn = QtGui.QPushButton('OK')
		self.cancelBtn = QtGui.QPushButton('Cancel')
		grid.addWidget(self.okBtn, 1, 0)
		grid.addWidget(self.cancelBtn, 1, 1)
		self.connect(self.okBtn, QtCore.SIGNAL('clicked()'), self.react)
		self.connect(self.cancelBtn, QtCore.SIGNAL('clicked()'), self.react)
		self.setLayout(grid)
		with open('./style/dialog.css','r') as f:
			self.setStyleSheet(f.read())

	def react(self):
		sender = self.sender()
		if sender == self.okBtn:
			res = unicode(self.combo.currentText().toLocal8Bit(), 'utf-8', 'ignore')
			try:
				del self.options[self.short.index(res)]
			except ValueError:
				pass
			with codecs.open('./data/main.txt', 'w', 'utf-8') as f:
				f.write('\n'.join(self.options))
			self.done(1)
		else:
			self.done(0)
