import sys
import numpy as np
import requests
import csv
import sqlite3
# count the arguments
class DataInit(object):

    def __init__(self):
        return None

    @staticmethod
    def getData():

        unicode()
        dates = ["03-22-2020","03-23-2020","03-24-2020","03-25-2020","03-26-2020","03-27-2020","03-28-2020","03-29-2020",
                 "03-30-2020","03-31-2020", "04-01-2020", "04-02-2020", "04-03-2020", "04-04-2020", "04-05-2020",
                 "04-06-2020", "04-07-2020", "04-08-2020", "04-09-2020", "04-10-2020", "04-11-2020", "04-12-2020",
                 "04-13-2020","04-14-2020","04-15-2020","04-16-2020","04-17-2020","04-18-2020","04-19-2020"
                 ,"04-20-2020" ,"04-21-2020","04-22-2020","04-23-2020","04-24-2020","04-25-2020","04-26-2020"
                 ,"04-27-2020","04-28-2020","04-29-2020","04-30-2020","05-01-2020","05-02-2020","05-03-2020"
                 ,"05-04-2020","05-05-2020","05-06-2020","05-07-2020","05-08-2020","05-09-2020","05-10-2020"
                 ,"05-11-2020","05-12-2020","05-13-2020","05-14-2020","05-15-2020","05-16-2020","05-17-2020"
                 ,"05-18-2020" ,"05-19-2020","05-20-2020","05-21-2020","05-22-2020","05-23-2020","05-24-2020"
                 ,"05-25-2020","05-26-2020","05-27-2020","05-28-2020","05-29-2020","05-30-2020","05-31-2020"
                 , "06-01-2020", "06-02-2020", "06-03-2020", "06-04-2020"]
        key = "Multnomah, Oregon, US"
        #Kittitas
        con = sqlite3.connect(":memory:")
        con.text_factory = str
        cur = con.cursor()
        cur.execute("CREATE TABLE t (FIPS, Admin2, Province_State, Country_Region, Last_Update, Lat, Long_, Confirmed, Deaths, Recovered, Active, Combined_Key);")  # use your column names here
        for j in range(len(dates)):
            with open('..\\COVID-19\\csse_covid_19_data\\csse_covid_19_daily_reports\\'+dates[j]+'.csv', 'rb') as fin:  # `with` statement available in 2.5+
                # csv.DictReader uses first line in file for column headings by default
                dr = csv.DictReader(fin)  # comma is default delimiter
                to_db = [( i['Admin2'], i['Province_State'], i['Country_Region'], i['Last_Update'], i['Lat'], i['Long_'], i['Confirmed'], i['Deaths'], i['Recovered'], i['Active'], i['Combined_Key']) for i in dr]
                cur.executemany("INSERT INTO t ( Admin2, Province_State, Country_Region, Last_Update, Lat, Long_, Confirmed, Deaths, Recovered, Active, Combined_Key) VALUES (?, ?,?,  ?,?,?,?,  ?,?,?,?);", to_db)


        con.commit()
        return con, dates, key

