
import matplotlib.pyplot as plt
from DataInit import DataInit


database, dates, key = DataInit.getData()


#covid_data = DataInit.getData()
g_colors = ["g", "r", "b", "c", "m", "y", "k", ]


firstDate = dates[0]
lastDate = dates[-1]
dataCases = []
dataDeaths = []
dataRecovered = []
dataDates = []



cur = database.cursor()

#   cur.execute("" \
#          "SELECT Confirmed, Recovered, Deaths " \
#         "FROM t " \
#        "WHERE Combined_Key = ? AND Last_Update LIKE ?", (key, date + '%'))
cur.execute("" \
        "SELECT Confirmed, Recovered, Deaths, Last_Update " \
        "FROM t " \
        "WHERE Combined_Key = ?",(key,))

rows = cur.fetchall()

for row in rows:
    dataCases.append(int(row[0]))
    dataRecovered.append(int(row[1]))
    dataDeaths.append(int(row[2]))
    date = row[3]
    date = date[:date.index(' ')]
    date = date.replace('03-', '3-')
    date = date.replace('3/', '3-')
    date = date.replace('2020-', '')
    date = date.replace('/20', '')
    print(date)
    dataDates.append(date)

print(rows)
print(dataCases)
#dataCases = [19,21,25,33,45,67,81,91,100]
print(dataCases)
#dataDeaths = [1,1,2,2,2,2,2,2,2]
#dataRecovered = [0,0,0,0,0,0,0,0,0]
#dates = [22,23,24,25,26,27,28,29,30]





plt.xlabel("Days")
plt.ylabel("Cases")
plt.xdate = True
plt.title("%s, from %s to %s" % (key, firstDate, lastDate))
_label0 = "Cases" #nice formating
plt.plot(dataDates, dataCases, color=g_colors[0], label=_label0)
_label1 = "Recoveries"   # nice formating
plt.plot(dataDates, dataRecovered, color=g_colors[1], label=_label1)
_label2 = "Deaths"  # nice formating
plt.plot(dataDates, dataDeaths, color=g_colors[2], label=_label2)

date_str = str(dates[-1])
s_folder = "covid_charts"
f = "Covid-19" + date_str
plt.legend(loc="best")
plt.figure()
plt.show()