import pandas as pd
import requests
from bs4 import BeautifulSoup
import datetime as dt
world = {}
coronavirus_cases = []
deaths = []
recovered = []
country_name = ['world']
final_url = ['https://www.worldometers.info/coronavirus']

# creating a dictionary  and assigning  keys and values
def datas():
    today_date = dt.date.today()
    world['countrys'] = country_name[0:num]
    world['Date'] = today_date
    world['covidcases'] = coronavirus_cases
    world['death'] = deaths
    world['recovered'] = recovered
    return world

# Collecting all countrys links and names in this function and saved in respective lists
def country():
    url = 'https://www.worldometers.info/coronavirus'
    page = requests.get(url)
    page.raise_for_status()
    soup = BeautifulSoup(page.text, 'html.parser')
    cnames = soup.find_all(class_='mt_a')
    for items in cnames:
        link = items.get('href')
        country_name.append(items.text)
        final_url.append('https://www.worldometers.info/coronavirus/' + link)

# collecting data from the final_url list and extracting and converting str values into int and float if there are numarical values
def urls(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    names = soup.find_all(class_='maincounter-number')
    tex = []
    for items in names:
        a = str(items.text.strip())
        if a  != 'N/A' :
            b = int(a.replace(',',''))
            tex.append(b)
        else:
            tex.append(0)
    return tex

# seperating the data into there list
def store(texs):
    coronavirus_cases.append(texs[0])
    deaths.append(texs[1])
    recovered.append(texs[2])
    return None

# data starts
country()
num = 50  # int (input("how many countrys do u wana see:")) we can use this command to to enter howmany values u want to see the data
num = num + 1
for i in range(num):
    page = urls(final_url[i])
    store(page)
data = datas()
df = pd.DataFrame(data)
s = str(dt.date.today()) + ".xlsx"
df.to_excel( s, sheet_name='covid_data', index=False)# converting the data frame to excel format every day
previousdata = pd.read_csv(r"Covid_data\coviddata.csv")
df = df.append(previousdata)
df.to_csv("Covid_data\\coviddata.csv",index = False)# combine all the data into one csv file 
