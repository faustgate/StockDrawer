#!/usr/bin/python
# simple.py

import sys
import os
import math
import ua_cross_bank as uacb
import ua_market as uam
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
        self.pB.clicked.connect(self.draw_cross)
        self.pushButton.clicked.connect(self.draw_market)
        self.today = dt.datetime.now()

    def plot(self):
        ''' plot some random stuff '''
        # make up some data
        x = [dt.datetime.now() + dt.timedelta(hours=i) for i in range(12)]
        y = [i + random.gauss(0, 1) for i, _ in enumerate(x)]

        # plot
        self.mplwidget.axes.plot(x, y)
        # beautify the x-labels
        self.mplwidget.figure.autofmt_xdate()

        # plt.show()
        self.mplwidget.axes.hold(False)

        # refresh canvas
        self.mplwidget.draw()

    def draw_graph(self, widget):

        self.mplwidget_2.axes.cla()
        self.mplwidget_2.axes.hold(True)
        self.mplwidget_2.axes.grid(True)

        ask = self.mplwidget_2.axes.plot_date(time_lines, ask_rates, '-b')
        ask = self.mplwidget_2.axes.plot_date(time_lines, bid_rates, '-r')
        #self.mplwidget_2.figure.autofmt_xdate()
        self.mplwidget_2.axes.set_title("USD")
        self.mplwidget_2.axes.legend(ask, labels=['test', 'test2'])

        # plt.show()

        # refresh canvas
        self.mplwidget_2.draw()

    def draw_market(self):
        rates = uam.get_rates()
        today_rates = []
        bid_rates = []
        ask_rates = []
        time_lines = []
        for index in range(len(rates)-1, -1, -1):
            try:
                dt.datetime.strptime(rates[index]['date'], "%H:%M")
            except ValueError:
                break
            else:
                today_rates.append(rates[index])

        today_rates.reverse()

        for rate in today_rates:
            bid_rates.append(rate['bid'])
            ask_rates.append(rate['ask'])
            rate_time = dt.datetime.strptime(rate['date'], "%H:%M")
            time_lines.append(self.today.replace(hour=rate_time.hour,
                                                 minute=rate_time.minute))
        self.mplwidget_2.axes.cla()
        self.mplwidget_2.axes.hold(True)
        self.mplwidget_2.axes.grid(True)

        ask = self.mplwidget_2.axes.plot_date(time_lines, ask_rates, '-b')
        ask = self.mplwidget_2.axes.plot_date(time_lines, bid_rates, '-r')
        #self.mplwidget_2.figure.autofmt_xdate()
        self.mplwidget_2.axes.set_title("USD")
        self.mplwidget_2.axes.legend(ask, labels=['test', 'test2'])

        # plt.show()

        # refresh canvas
        self.mplwidget_2.draw()

    def draw_cross(self):
        rates = uacb.get_rates()
        today_rates = []
        bid_rates = []
        ask_rates = []
        time_lines = []
        for index in range(len(rates)-1, -1, -1):
            try:
                dt.datetime.strptime(rates[index]['date'], "%H:%M")
            except ValueError:
                break
            else:
                today_rates.append(rates[index])

        today_rates.reverse()

        for rate in today_rates:
            bid_rates.append(rate['bid'])
            ask_rates.append(rate['ask'])
            rate_time = dt.datetime.strptime(rate['date'], "%H:%M")
            time_lines.append(self.today.replace(hour=rate_time.hour,
                                                 minute=rate_time.minute))

        self.mplwidget.axes.cla()
        self.mplwidget.axes.hold(True)
        self.mplwidget.axes.grid(True)

        ask = self.mplwidget.axes.plot_date(time_lines, ask_rates, '-b')
        ask = self.mplwidget.axes.plot_date(time_lines, bid_rates, '-r')
        #self.mplwidget_2.figure.autofmt_xdate()
        self.mplwidget.axes.set_title("USD")
        self.mplwidget.axes.legend(ask, labels=['test', 'test2'])

        # plt.show()

        # refresh canvas
        self.mplwidget.draw()

app = QtGui.QApplication(sys.argv)
renamer = Renamer()
renamer.show()
sys.exit(app.exec_())


