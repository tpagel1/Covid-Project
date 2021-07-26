import csv
import json
import couchdb
import matplotlib.pyplot as plt
import holoviews as hv
from holoviews import opts
hv.extension('bokeh')

import numpy as np 
import pandas as pd 
from bokeh.plotting import figure, output_file, output_notebook, show


with open("Data.json") as f:
    Data = json.load(f)

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

        
       
#create lists for dates, cases, Percent
Dates=[]
NSW=[]
VIC=[]
NT=[]
TAS=[]
WA=[]
ACT=[]
SA=[]
NSWP=[]

for item in Data:
    Dates.append(str(item))
    NSW.append(float(((Data[item]["New South Wales"]*1000000)/Population["NSW"])))
    VIC.append(float(((Data[item]["Victoria"]*1000000)/Population["VIC"])))
    NT.append(float(((Data[item]["Northern Territory"]*1000000)/Population["NT"])))
    TAS.append(float(((Data[item]["Tasmania"]*1000000)/Population["TAS"])))
    WA.append(float(((Data[item]["Western Australia"]*1000000)/Population["WA"])))
    ACT.append(float(((Data[item]["Australian Capital Territory"]*1000000)/Population["Australian Capital Territory"])))
    SA.append(float(((Data[item]["South Australia"]*1000000)/Population["SA"])))

for item in Data:
    if Data[item]["Total"]==0:
        NSWP.append(float(0))
    else:
        NSWP.append((Data[item]["Related"]/Data[item]["Total"])*100)



#Graph Daily state cases per 1 million population against percentage of tweets regarding coronavirus

graph= figure(title="Cases vs percent")

NSWline = hv.Curve((NSW), label='NSW')
VICline = hv.Curve((VIC), label='VIC')
NTline = hv.Curve((NT), label='NT')
TASline = hv.Curve((TAS), label='TAS')
WAline = hv.Curve((WA), label='WA')
ACTline = hv.Curve((ACT), label='ACT')
SAline = hv.Curve((SA), label='SA')

line2 = hv.Curve((NSWP), label='Percent')

graph = (NSWline * VICline * NTline * TASline * WAline * ACTline * line2).opts(width=600, legend_position='top_left', xticks=[(0,Dates[0]),(30,Dates[30]),(60,Dates[60]),(90,Dates[90]),(120,Dates[120])])

outfp= "graph.html"
output_file(outfp)
hv.save(graph,"graph.html",fmt="auto")
