
import matplotlib.pyplot as plt
from DataInit import DataInit
from matplotlib.ticker import (
    AutoLocator, AutoMinorLocator)
import datetime
import matplotlib.dates as mdates
import numpy as np
from matplotlib.transforms import Transform
import matplotlib.ticker as ticker
import os


database, dates, key = DataInit.getData()
try:
    os.mkdir("C:\Users\Will Regan\Desktop\covid/"+ key)
except OSError as error:
    print(error)

#covid_data = DataInit.getData()
g_colors = ["g", "r", "b", "c", "m", "y", "k", ]


firstDate = dates[0]
lastDate = dates[-1]
dataCases = []
data7avg = []
data14avg = []
data30avg = []

dataDeaths = []
dataActive = []

dataDates = []
dataDailyCases = []
dataPercentIncrease = []



cur = database.cursor()

#   cur.execute("" \
#          "SELECT Confirmed, Recovered, Deaths " \
#         "FROM t " \
#        "WHERE Combined_Key = ? AND Last_Update LIKE ?", (key, date + '%'))
cur.execute("" \
        "SELECT Confirmed, Active, Deaths, Last_Update " \
        "FROM t " \
        "WHERE Combined_Key = ?",(key,))

rows = cur.fetchall()
last = 0
count = 0
for row in rows:
    count += 1

    active = int(row[1])
    if count < 23 and active == 0:
        active = int(row[0]) - int(row[2])



    dataCases.append(int(row[0]))

    daily = int(row[0]) - last
    dataDailyCases.append(daily)

    num = 1
    total = 0
    avg = 0
    while num < 8:
       if len(dataDailyCases) > num - 1:
           total += dataDailyCases[-1 * num]
           num += 1
       else:
           num = 8

    avg = total / num
    data7avg.append(avg)

    num = 1
    total = 0
    avg = 0
    while num < 15:
       if len(dataDailyCases) > num - 1:
           total += dataDailyCases[-1 * num]
           num += 1
       else:
           num = 15

    avg = total / num
    data14avg.append(avg)

    num = 1
    total = 0
    avg = 0
    while num < 30:
        if len(dataDailyCases) > num - 1:
            total += dataDailyCases[-1 * num]
            num += 1
        else:
            num = 30

    avg = total / num
    data30avg.append(avg)


    dataActive.append(active)
    dataDeaths.append(int(row[2]))
    if last == 0:
        last = int(row[0])

    if last == 0:
        last = 1
    dataPercentIncrease.append(float(daily)/last)
    last = float(int(row[0]))
    date = row[3]
    date = date[:date.index(' ')]
    print(date)
   # if count % 2 == 0:
    dataDates.append(date)

print(rows)
print(dataCases)
#dataCases = [19,21,25,33,45,67,81,91,100]
print(dataCases)

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

fig, ax = plt.subplots(constrained_layout=True)

ax.set_xlabel("Days")
ax.set_ylabel("New Cases Moving Average")
ax.xdate = True
ax.set_title("%s, from %s to %s" % (key, firstDate, lastDate))
_label0 = "7 day average new cases" #nice formating
ax.plot(dates, data7avg, color=g_colors[0], label=_label0)
_label1 = "14 day average new cases" #nice formating
ax.plot(dates, data14avg, color=g_colors[1], label=_label1)
_label2 = "30 day average new cases" #nice formating
ax.plot(dates, data30avg, color=g_colors[2], label=_label2)
ax.legend(loc="best")

ax.format_xdata = mdates.DateFormatter('%m-%d')
fig.autofmt_xdate()

dates_cp = dates[:]

dates = [datetime.datetime(2020, 3, 23) + datetime.timedelta(hours=k * 24)
            for k in range(count-1)]

plt.savefig("C:\Users\Will Regan\Desktop\covid/"+ key + "/mvgAvg")

fig, ax = plt.subplots(constrained_layout=True)

ax.set_xlabel("Days")
ax.set_ylabel("New Cases")
ax.xdate = True
ax.set_title("%s, from %s to %s" % (key, firstDate, lastDate))
_label0 = "New Cases" #nice formating
dataDates.pop(0)
dataDailyCases.pop(0)
ax.bar(dates, dataDailyCases, color=g_colors[0], label=_label0)
ax.legend(loc="best")

ax.format_xdata = mdates.DateFormatter('%m-%d')
fig.autofmt_xdate()
plt.savefig("C:\Users\Will Regan\Desktop\covid/"+ key + "/newCases")
plt.figure()

fig, ax = plt.subplots(constrained_layout=True)

ax.set_xlabel("Days")
ax.set_ylabel("New Day Percent Increase")
ax.xdate = True
ax.set_title("%s, from %s to %s" % (key, firstDate, lastDate))
_label0 = "Percent" #nice formating
dataPercentIncrease.pop(0)
ax.plot(dates, dataPercentIncrease, color=g_colors[0], label=_label0)
ax.legend(loc="best")

ax.format_xdata = mdates.DateFormatter('%m-%d')
fig.autofmt_xdate()

plt.savefig("C:\Users\Will Regan\Desktop\covid/"+ key + "/percent")
plt.figure()

fig, ax = plt.subplots(constrained_layout=True)

ax.xdate = True
ax.set_title("%s, from %s to %s" % (key, firstDate, lastDate))
ax.set_xlabel("Days")
ax.set_ylabel("New Cases")

x = np.arange(len(dates_cp))
y = data14avg


coefficients = np.polyfit(x, y, 3)
poly = np.poly1d(coefficients)
new_x = np.linspace(x[0], x[-1])
new_y = poly(new_x)

ax.plot(x, y, "o", new_x, new_y)
ax.set_xlim([x[0]-1, x[-1] + 1 ])


plt.xticks(np.arange(len(dates_cp)), dates_cp, rotation=30)

spacing = 0
for label in ax.get_xticklabels()[:]:
    spacing += 1
    if spacing % 8 != 0:
       label.set_visible(False)


ax.legend(loc="best")


plt.savefig("C:\Users\Will Regan\Desktop\covid/"+ key + "/14dayFit")



fig, ax = plt.subplots(constrained_layout=True)

ax.xdate = True
ax.set_title("%s, from %s to %s" % (key, firstDate, lastDate))
ax.set_xlabel("Days")
ax.set_ylabel("New Cases")

x = np.arange(len(dates_cp))
y = data7avg


coefficients = np.polyfit(x, y, 3)
poly = np.poly1d(coefficients)
new_x = np.linspace(x[0], x[-1])
new_y = poly(new_x)

ax.plot(x, y, "o", new_x, new_y)
ax.set_xlim([x[0]-1, x[-1] + 1 ])


plt.xticks(np.arange(len(dates_cp)), dates_cp, rotation=30)

spacing = 0
for label in ax.get_xticklabels()[:]:
    spacing += 1
    if spacing % 8 != 0:
       label.set_visible(False)


ax.legend(loc="best")


plt.savefig("C:\Users\Will Regan\Desktop\covid/"+ key + "/7dayFit")

fig, ax = plt.subplots(constrained_layout=True)

ax.xdate = True
ax.set_title("%s, from %s to %s" % (key, firstDate, lastDate))
ax.set_xlabel("Days")
ax.set_ylabel("New Cases")

x = np.arange(len(dates_cp))
y = data30avg


coefficients = np.polyfit(x, y, 3)
poly = np.poly1d(coefficients)
new_x = np.linspace(x[0], x[-1])
new_y = poly(new_x)

ax.plot(x, y, "o", new_x, new_y)
ax.set_xlim([x[0]-1, x[-1] + 1 ])


plt.xticks(np.arange(len(dates_cp)), dates_cp, rotation=30)

spacing = 0
for label in ax.get_xticklabels()[:]:
    spacing += 1
    if spacing % 8 != 0:
       label.set_visible(False)


ax.legend(loc="best")


plt.savefig("C:\Users\Will Regan\Desktop\covid/"+ key + "/30dayFit")


plt.show()