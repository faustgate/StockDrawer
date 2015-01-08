#!/usr/bin/python
# -*- coding: UTF-8 -*-

from datetime import date

import pylab
import matplotlib.dates


if __name__ == "__main__":
    # Даты, которые будут отложены по оси X
    xdata = [date(2010, 5, 25),
             date(2010, 7, 5),
             date(2010, 12, 1),
             date(2011, 3, 17),
             date(2011, 8, 2),
             date(2011, 11, 13),
             date(2012, 3, 15),
             date(2012, 4, 8),
             date(2012, 12, 21)
    ]

    # Данные, которые будут отложены по оси Y
    ydata = [0.4, 0.3, 0.5, 0.4, 0.6, 0.3, 0.2, 0.1, 0.0]

    # Преобразуем даты в числовой формат
    xdata_float = matplotlib.dates.date2num(xdata)

    # Вызовем subplot явно, чтобы получить экземпляр класса AxesSubplot,
    # из которого будем иметь доступ к осям
    axes = pylab.subplot(1, 1, 1)

    # Пусть в качестве меток по оси X выводится только год
    axes.xaxis.set_major_formatter(matplotlib.dates.DateFormatter("%d.%m.%Y"))

    # Отобразим данные
    pylab.plot_date(xdata_float, ydata, fmt="b-")

    pylab.grid()
    pylab.show()