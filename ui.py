#!/usr/bin/python
# simple.py

import sys
import os
import math
import main
import requests
import time
import json
import execjs
from PyQt4 import QtCore, QtGui, uic
from PyKDE4.kdeui import KPushButton, KLineEdit, KPlotWidget, KTextBrowser, \
    KPlotObject


class Renamer(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)

        # widget.resize(250, 150)
        # widget.setWindowTitle('simple')
        uic.loadUi('graph.ui', self)
        self.kplotwidget.setLimits(0, 20, 0, 20)
        self.kplotwidget.axis(KPlotWidget.BottomAxis).setLabel(
            'Angle in radians')
        self.kplotwidget.axis(KPlotWidget.LeftAxis).setLabel(
            'Angle in degress')
        self.kplotwidget.setAntialiasing(True)
        self.sineobj = KPlotObject(QtGui.QColor(10, 50, 255),
                                   KPlotObject.Lines, 2)
        self.coseobj = KPlotObject(QtGui.QColor(255, 50, 10),
                                   KPlotObject.Lines, 2)

        start = 0
        finish = 50
        step = 0.001
        x = start
        cur_rate = main.get_rates()
        # while x <= finish:
        self.sineobj.addPoint(10, float(cur_rate['bid']))
        self.sineobj.addPoint(15, float(cur_rate['bid']))

        #     self.coseobj.addPoint(x, math.cos(x))
        #     x += step


        self.kplotwidget.addPlotObject(self.sineobj)
        #self.kplotwidget.addPlotObject(self.coseobj)
        self.kplotwidget.update()

app = QtGui.QApplication(sys.argv)
renamer = Renamer()
renamer.show()
sys.exit(app.exec_())


