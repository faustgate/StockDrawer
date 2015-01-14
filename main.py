#!/usr/bin/python
# simple.py

import sys
import os
import math
from threading import Timer
import ukraine
import requests
import time
import json
import execjs
import datetime as dt
import random
from PyQt4 import QtCore, QtGui, uic
from PyKDE4.kdeui import KPushButton, KLineEdit, KPlotWidget, KTextBrowser, \
    KPlotObject
from matplotlib.backends.backend_qt4agg import \
    FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import \
    NavigationToolbar2QTAgg as NavigationToolbar
from matplotlib.dates import MinuteLocator
import matplotlib.pyplot as plt
import matplotlib.dates
from matplotlib.figure import Figure
import matplotlibwidget


class Renamer(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)

        # widget.resize(250, 150)
        # widget.setWindowTitle('simple')
        uic.loadUi('graph.ui', self)
        self.btn_Plot.clicked.connect(self.plot)
        #self.pB.clicked.connect(self.draw_cross)
        self.pushButton.clicked.connect(self.draw_ukraine)
        self.today = dt.datetime.now()

    def plot(self):
        ''' plot some random stuff '''
        # make up some data
        x = [dt.datetime.now() + dt.timedelta(hours=i) for i in range(4)]
        y = [i + random.gauss(0, 1) for i, _ in enumerate(x)]

        # plot
        self.mplwidget.axes.plot(x, y)
        # beautify the x-labels
        self.mplwidget.figure.autofmt_xdate(hspace=5)

        # plt.show()
        self.mplwidget.axes.hold(False)

        # refresh canvas
        self.mplwidget.draw()

    def parse(self, source):
        today_rates = []
        bid_rates = []
        ask_rates = []
        time_lines = []
        for index in range(len(source)-1, -1, -1):
            try:
                dt.datetime.strptime(source[index]['date'], "%H:%M")
            except ValueError:
                break
            else:
                today_rates.append(source[index])

        today_rates.reverse()

        for rate in today_rates:
            bid_rates.append(rate['bid'])
            ask_rates.append(rate['ask'])
            rate_time = dt.datetime.strptime(rate['date'], "%H:%M")
            time_lines.append(self.today.replace(hour=rate_time.hour,
                                                 minute=rate_time.minute))
        return bid_rates, ask_rates, time_lines

    def draw(self, widget, source_date, title):
        bid_rates, ask_rates, time_lines = self.parse(source_date)
        widget.axes.cla()
        widget.axes.hold(True)
        widget.axes.grid(True)

        ask = widget.axes.plot_date(time_lines, ask_rates, '-b')
        ask = widget.axes.plot_date(time_lines, bid_rates, '-r')
        #self.mplwidget_2.figure.autofmt_xdate()
        widget.axes.set_title(title)
        widget.axes.legend(ask, labels=['test', 'test2'])

        # plt.show()

        # refresh canvas
        widget.draw()

    def draw_ukraine(self):
        rates = ukraine.get_rates()
        for key in rates:
            widget_name = getattr(self, key)
            self.draw(widget_name, rates[key], key.replace('_', " ").upper())
        Timer(60.0, self.draw_ukraine).start()

app = QtGui.QApplication(sys.argv)
renamer = Renamer()
renamer.show()
sys.exit(app.exec_())


