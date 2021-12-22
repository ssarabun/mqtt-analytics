# импортируем модули
import matplotlib as mpl
mpl.use('Agg')

import matplotlib.pyplot as plt
import matplotlib.dates as dates


import numpy as np
import io
import base64
from datetime import datetime
import matplotlib.dates as mdates



def data_to_chart(label, counter_data, td):
    print(f'td={td}')
    if len(counter_data) == 0:
        return None

    x_array = [ row['created'] for row in counter_data]
    y_array = [row['counter_value'] for row in counter_data]

    plt.figure()

    # создаём рисунок с координатную плоскость
    fig, ax = plt.subplots(1, 1, figsize=(12, 4), constrained_layout=True)

    plt.title(f"Chart: {label}")

#     ax.xlabel('period')
#     ax.ylabel('Loading')

    interval = 1
    if td == 'hour':
        if len(counter_data) > 27:
            interval = 4
        elif len(counter_data) > 16:
            interval = 2

        ax.xaxis.set_major_locator(dates.DayLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d %H:%M'))

        ax.xaxis.set_minor_locator(dates.HourLocator(interval=interval))
        ax.xaxis.set_minor_formatter(mdates.DateFormatter('%H:%M'))
    elif td == 'min':
        major_locator = dates.HourLocator()
        minor_locator = None
        if len(counter_data) >= 60 and len(counter_data) < 180:
            minor_locator = dates.MinuteLocator(interval = 5)
        elif len(counter_data) >= 180 and len(counter_data) < 360:
            minor_locator = dates.MinuteLocator(interval = 10)
        elif len(counter_data) >= 360 and len(counter_data) < 480:
            minor_locator = dates.MinuteLocator(interval = 15)
        elif len(counter_data) >= 480:
            minor_locator = dates.MinuteLocator(interval = 30)
        else:
            minor_locator = dates.MinuteLocator(interval = 5)


        ax.xaxis.set_major_locator(major_locator)
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d %H:%M'))

        ax.xaxis.set_minor_locator(minor_locator)
        ax.xaxis.set_minor_formatter(mdates.DateFormatter('%H:%M'))

    for label in ax.get_xticklabels(which='both'):
        label.set(rotation=30, horizontalalignment='right')

    ax.plot(x_array, y_array)
    ax.grid(True)

    my_stringIObytes = io.BytesIO()
    plt.savefig(my_stringIObytes, format='png')
    my_stringIObytes.seek(0)
    my_base64_jpgData = base64.b64encode(my_stringIObytes.read())


    # показываем график
    #plt.show()

    return my_base64_jpgData.decode("utf-8")
