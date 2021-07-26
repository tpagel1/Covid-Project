import couchdb
import csv
import re
import json
import http.client
import urllib.request
import holoviews as hv
from holoviews import opts
hv.extension('bokeh')
from bokeh.plotting import figure, output_file, output_notebook, show

user = "admin"
couch = couchdb.Server("http://%s:%s@127.0.0.1:5984/" % (user,"12345"))
db = couch["bigtwittergeotweets"]

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
            Data[item][i[0]]={}
            Data[item][i[0]]["Cases"]=0
            Data[item][i[0]]["Tweets"]=0
            Data[item][i[0]]["Related"]=0

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
                Data[date][key]["Cases"]=state[j]
                j+=1
print("Hash created")
map='function (doc) { if (doc.location=="sydney") { emit(["New South Wales",doc._id,doc.text,doc.created_at], 1);}'
for row in db.query(map):
    print(row.key)

'''
keywords=["covid","corona","virus","quarantine","lockdown","socialdistancing","covid19","sarscov19","pandemic","isolation","wuhan","chinavirus"]
for item in db: 
    print("read")
    try:
        text = db[item]["text"].lower()
        text = re.sub('[#@-_*&$!]','',text)
        date = makeDate(db[item]["created_at"])
        state = getState(db[item]["location"]) 
        Data[date][state]["Tweets"]+=1
        print("line processed")
        for search in keywords:
            if re.search(search,text):
                Data[date][state]["Related"]+=1
                print('related found')
                break
        del item
    except (http.client.IncompleteRead) as e:
        item=e.partial
        print("incomplete read")
        continue

Population={}
with open("populationcapstate.csv","r") as p:
    reader = csv.reader(p, delimiter=',')
    p.readline()
    for row in reader:
        Population[row[3]]=int(row[0])

Population["NSW"]=Population["Greater Sydney"]+Population["Rest of NSW"]
Population["VIC"]=Population["Greater Melbourne"]+Population["Rest of Vic."]
Population["QLD"]=Population["Greater Brisbane"]+Population["Rest of Qld"]
Population["SA"]=Population["Greater Adelaide"]+Population["Rest of SA"]
Population["WA"]=Population["Greater Perth"]+Population["Rest of WA"]
Population["TAS"]=Population["Greater Hobart"]+Population["Rest of Tas."]
Population["NT"]=Population["Greater Darwin"]+Population["Rest of NT"]
Population["ACT"]=Population["Australian Capital Territory"]

def makeGraph(string):
    States={}
    States["WA"]="Western Australia"
    States["QLD"]="Queensland"
    States["ACT"]="Australian Capital Territory"
    States["NSW"]="New South Wales"
    States["VIC"]="Victoria"
    States["TAS"]="Tasmania"
    States["NT"]="Northern Territory"
    States["SA"]="South Australia"
    name = States[string]
    cases=[]
    Dates=[]
    Percent=[]
    for item in Data:
        Dates.append(str(item))
        cases.append(float(((Data[item][name]["Cases"]*1000000)/Population[string])))
        if Data[item][name]["Tweets"]==0:
            Percent.append(float(0))
        else:
            Percent.append((Data[item][name]["Related"]/Data[item][name]["Tweets"])*100)
    caseLine = hv.Curve((cases), label=str(string)+ " daily cases per million")
    percentLine = hv.Curve((Percent), label=str(string)+" percentage related tweets")
    graph= (caseLine * percentLine).opts(width=600, legend_position='top_left', xticks=[(0,Dates[0]),(30,Dates[30]),(60,Dates[60]),(90,Dates[90]),(120,Dates[120])])
    outfp= ("/htmloutput/"+str(string)+"covid.html")
    output_file(outfp)
    hv.save(graph,outfp,fmt="auto")

makeGraph("NSW")
makeGraph("QLD")
makeGraph("VIC")
makeGraph("NT")
makeGraph("SA")
makeGraph("WA")
makeGraph("TAS")
makeGraph("ACT")
'''