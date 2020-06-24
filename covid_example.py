
import matplotlib.pyplot as plt
from DataInit import DataInit
from matplotlib.ticker import (
    AutoLocator, AutoMinorLocator)
import datetime
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import os


database, dates, key = DataInit.getData()
try:
    os.mkdir("C:\Users\Will Regan\Desktop\covid/"+ key)
except OSError as error:
    print(error)

g_colors = ["g", "r", "b"]


firstDate = dates[0]
lastDate = dates[-1]
dataCases = []
dataDeaths = []
dataActive = []


cur = database.cursor()


cur.execute("" \
        "SELECT Confirmed, Active, Deaths, Last_Update " \
        "FROM t " \
        "WHERE Combined_Key = ?",(key,))

rows = cur.fetchall()

count = 0

for row in rows:
    count += 1
    dataCases.append(int(row[0]))

    active = int(row[1])
    if count < 23 and active == 0:
        active = int(row[0]) - int(row[2])

    dataActive.append(active)
    dataDeaths.append(int(row[2]))


dates = [datetime.datetime(2020, 3, 22) + datetime.timedelta(hours=k * 24)
            for k in range(count)]

fig, ax = plt.subplots(constrained_layout=True)

plt.xticks(rotation=70)

ax.set_xlabel("Days")
ax.set_ylabel("Total Cases")
ax.xdate = True
ax.set_title("%s, from %s to %s" % (key, firstDate, lastDate))
_label0 = "Total Cases" #nice formating
ax.plot(dates, dataCases, color=g_colors[0], label=_label0)
_label1 = "Active"   # nice formating
ax.plot(dates, dataActive, color=g_colors[1], label=_label1)
_label2 = "Deaths"  # nice formating
ax.plot(dates, dataDeaths, color=g_colors[2], label=_label2)

ax.format_xdata = mdates.DateFormatter('%m-%d')
fig.autofmt_xdate()

ax.legend(loc="best")
plt.savefig("C:\Users\Will Regan\Desktop\covid/"+ key + "/totalCases")
plt.figure()

plt.show()