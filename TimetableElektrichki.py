import requests
from bs4 import BeautifulSoup
import datetime


date = datetime.datetime.now()

URL_osip_minsk = "http://mogilev.elektrichki.net/raspisanie/" \
      "osipovichi-1/minsk/{}/".format(date.strftime("%d-%m-%Y"))
URL_minsk_osip = "http://minsk.elektrichki.net/raspisanie/" \
      "minsk/osipovichi-1/{}/".format(date.strftime("%d-%m-%Y"))


def get_timetable(url, file_name):

    sourse_code = requests.get(url)
    soup = BeautifulSoup(sourse_code.text)

    train_number = soup.findAll(name="span", attrs={
        "class": "train_number"})
    timetable_time = soup.findAll(name="div", attrs={
        "class": "timetable_time"})
    timetable_pathtime = soup.findAll(name="div", attrs={
        "class": "timetable_pathtime"})

    timetable = {"number": [], "time1": [], "time2": [], "pathtime": []}

    for train in range(len(train_number)):
        timetable["number"].append(train_number[train].string)
        timetable["time1"].append(timetable_time[train*2].string)
        timetable["time2"].append(timetable_time[train*2+1].string)
        timetable["pathtime"].append(timetable_pathtime[train*2].string)

    file = open(file_name, "w")

    for i in range(len(train_number)):
        file.write("{} :: {} :: {} --- {} :: {}\n".format(
            date.strftime("%d-%m-%Y"), timetable["number"][i], timetable["time1"][i],
            timetable["time2"][i], timetable["pathtime"][i]))


get_timetable(URL_osip_minsk, "OsipToMinsk")
get_timetable(URL_minsk_osip, "MinskToOsip")