"""
The University of Melbourne
COMP90024: Cluster and Cloud Computing
Semester 1 2020
Assignment 2: City Analytics on the Cloud
Group 69
Wei He 835655
Marc Nguyen 350899
Tom Pagel 10637290
Toby Profitt 761991
Sebastian Winter 685124
"""
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

#Accessing the couchDB server and references the correct dB.
user = "admin"
couch = couchdb.Server("http://%s:%s@172.26.131.239:5984/" % (user,"admin"))
db = couch["mydb"]

#requests covid data from github every time so it is always totally up to date
data = []
url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
with urllib.request.urlopen(url) as f:
    for row in f:
        data.append(row.decode(('utf-8')).rstrip().split(","))

#takes the format of date from the twitter json file and converts it into a key string for my data hash
def makeDate(x):
    Months={}
    Months["Jan"]=1
    Months["Feb"]=2
    Months["Mar"]=3
    Months["Apr"]=4
    Months["May"]=5
    month = str(x[4:7])
    month = Months[month]
    day = int(str(x[8:10]))
    date=str(month)+"/"+str(day)+"/20"
    return date

#takes location string from json data and outputs correct state
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

#this section pre processes that covid case data into the format required
aus =[]
daily = []
n=[0,9,10,11,12,13,14,15,16]
Data={}
for i in n:
    aus.append(data[i])  
for i in aus:
    del i[1:4]
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

#list of covid related keywords with the more popular near the front of the list so that the program can break before looping through this list too many times
keywords=["covid","corona","virus","quarantine","lockdown","socialdistancing","covid19","sarscov19","pandemic","isolation","wuhan","chinavirus"]

#Tweet processing, testing relevance and putting it correct place in Data hash
for item in db: 
    try:
        text = db[item]["text"].lower()
        text = re.sub('[#@-_*&$!]','',text)
        date = makeDate(db[item]["created_at"])
        state = getState(db[item]["location"]) 
        Data[date][state]["Tweets"]+=1
        for search in keywords:
            if re.search(search,text):
                Data[date][state]["Related"]+=1
                print('related found')
                break
    except:
        continue
   
print(Data)

#importing population data from AURIN
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

#takes a string code for a state and outputs HoloViews interactive graph with daily case line and tweet related line
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
    graph= (caseLine * percentLine).opts(width=600, legend_position='top_left', xticks=[(0,Dates[0]),(20,Dates[20]),(40,Dates[40]),(60,Dates[60]),(80,Dates[80]),(100,Dates[100])])
    outfp= ("/htmloutput/"+str(string)+"covid.html")
    output_file(outfp)
    hv.save(graph,outfp,fmt="auto")

makeGraph("NSW")
makeGraph("QLD")
makeGraph("NT")
makeGraph("SA")
makeGraph("WA")
makeGraph("TAS")
makeGraph("ACT")
