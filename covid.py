from firebase import firebase
import requests
from bs4 import BeautifulSoup as bs
import datetime as dt
import schedule
import time

firebase = firebase.FirebaseApplication(
    'https://python-covid-72c3f.firebaseio.com/', None)


def covid():
    date = dt.date.today()
    dec = {'country': "india", "date": str(date)}
    url = 'https://www.worldometers.info/coronavirus/country/india/'
    page = requests.get(url)
    soup = bs(page.text, 'html.parser')
    table = soup.find_all('div', attrs={"id": "maincounter-wrap"})
    val = []
    for i in table:
        val.append((i.find("span")).text)
    dec["cases"] = val[0]
    dec["death"] = val[1]
    dec['recovered'] = val[2]
    data = firebase.post('/Covid/Data', dec)
    print(data)


schedule.every().day.at("03:00").do(covid)
print("Program run")

while True:
    schedule.run_pending()
    time.sleep(1)
