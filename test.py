import csv
import urllib.request

data = []
url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
with urllib.request.urlopen(url) as f:
    for row in f:
        data.append(row.decode(('utf-8')).rstrip().split(","))

aus =[]
n=[0,9,10,11,12,13,14,15,16]
for i in n:
    aus.append(data[i])
   
for i in aus:
    del i[1:4]

Data={}

for i in aus[0]:
    if i == aus[0][0]:
        continue
    else:
        Data[i]={}

for i in aus:
    for item in Data:
        if i == aus[0]:
            continue
        else:
            Data[item][i[0]]=0

daily = []
for i in range(1,len(aus)):
    temp=[]
    temp.append(aus[i][0])
    temp.append(int(0))
    for j in range(2,len(aus[i])):
        temp.append(int(aus[i][j])-int(aus[i][j-1]))
    daily.append(temp)

for state in daily:
    j=1
    while j<len(state):
        key=state[0]
        for date in Data:
            Data[date][key]=state[j]
            j+=1