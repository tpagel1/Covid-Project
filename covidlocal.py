import couchdb
import csv
import re
import json
import urllib.request
import holoviews as hv
from holoviews import opts
hv.extension('bokeh')
from bokeh.plotting import figure, output_file, output_notebook, show

user = "admin"
couch = couchdb.Server("http://%s:%s@127.0.0.1:5984/" % (user,12345))
db = couch["bigtwittergeotweets"]

State="New South Wales"
data = []
url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
with urllib.request.urlopen(url) as f:
    for row in f:
        data.append(row.decode(('utf-8')).rstrip().split(","))

def makeDate(x):
    Months={}
    Months["Mar"]=3
    Months["Apr"]=4
    Months["May"]=5
    Months["Jun"]=6
    month = str(x[4:7])
    month = Months[month]
    day = str(x[8:10])
    date=str(month)+"/"+day+"/20"
    return date

def getState(y):
    States={}
    States["perth"]="Western Australia"
    States["brisbane"]="Queensland"
    States["canberra"]="Australian Capital Territory"
    States["sydney"]="New South Wales"
    States["melbourne"]="Victoria"
    States["hobart"]="Tasmania"
    States["darwin"]="Northern Territory"
    States["adelaide"]="South Australia"
    return States[y]

def makeGraph(string):
    cases=[]
    Dates=[]
    Percent=[]
    for item in Data:
        Dates.append(str(item))
        cases.append(float(((Data[item]["Cases"]*1000000)/Population[string])))
        if Data[item]["Tweets"]==0:
            Percent.append(float(0))
        else:
            Percent.append((Data[item]["Related"]/Data[item]["Tweets"])*100)
    caseLine = hv.Curve((cases), label=str(string)+ " daily cases per million")
    percentLine = hv.Curve((Percent), label=str(string)+" percentage related tweets")
    graph= (caseLine * percentLine).opts(width=600, legend_position='top_left', xticks=[(0,Dates[0]),(30,Dates[30]),(60,Dates[60]),(90,Dates[90]),(120,Dates[120])])
    outfp= (str(string)+"covid.html")
    output_file(outfp)
    hv.save(graph,outfp,fmt="auto")

Population={}
with open("populationcapstate.csv","r") as p:
    reader = csv.reader(p, delimiter=',')
    p.readline()
    for row in reader:
        Population[row[3]]=int(row[0])

Population["New South Wales"]=Population["Greater Sydney"]+Population["Rest of NSW"]
Population["Victoria"]=Population["Greater Melbourne"]+Population["Rest of Vic."]
Population["Queensland"]=Population["Greater Brisbane"]+Population["Rest of Qld"]
Population["South Australia"]=Population["Greater Adelaide"]+Population["Rest of SA"]
Population["Western Australia"]=Population["Greater Perth"]+Population["Rest of WA"]
Population["Tasmania"]=Population["Greater Hobart"]+Population["Rest of Tas."]
Population["Northern Territory"]=Population["Greater Darwin"]+Population["Rest of NT"]


stateRow={}
stateRow["Queensland"]=12
stateRow["New South Wales"]=10
stateRow["Victoria"]=15
stateRow["Australian Capital Territory"]=9
stateRow["Western Australia"]=16
stateRow["Northern Territory"]=11
stateRow["Tasmania"]=14
stateRow["South Australia"]=15

dates=data[0]
aus = data[stateRow[State]]
del aus[1:4]
del dates[1:4]

Data={}
for i in dates:
    if i == dates[0]:
        continue
    else:
        Data[i]={}
        Data[i]["Cases"]=0
        Data[i]["Tweets"]=0
        Data[i]["Related"]=0

daily = []
daily.append(aus[0])
daily.append(int(0))
for j in range(2,len(aus)):
    daily.append(int(aus[j])-int(aus[j-1]))

i=1
while i < len(daily):
    for date in Data:
        Data[date]["Cases"]=daily[i]
        i+=1

keywords=["covid","corona","virus","quarantine","lockdown","socialdistancing","covid19","sarscov19","pandemic","isolation","wuhan","chinavirus"]
for item in db: 
        text = db[item]["doc"]["text"].lower()
        text = re.sub('[#@-_*&$!]','',text)
        try:
            date = makeDate(db[item]["doc"]["created_at"])
            Data[date]["Tweets"]+=1
        except:
            continue
        for search in keywords:
            try:
                if re.search(search,text):
                    date = makeDate(db[item]["doc"]["created_at"])
                    Data[date]["Related"]+=1
                    break
            except:
                continue

makeGraph(State)


