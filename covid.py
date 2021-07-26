import couchdb
import re
import csv

#access couchdb with user, password and which db
user = "admin"
couch = couchdb.Server("http://%s:%s@127.0.0.1:5984/" % (user,12345))
db = couch["bigtwittergeotweets"]
covid = couch["covidjanmarch"]

#create hashes
Dates={}
Dates["January"]={}
Dates["February"]={}
Dates["March"]={}

Months={}
Months["January"]={}
Months["February"]={}
Months["March"]={}

for month in Months:
    Months[month]["Total"]=0
    Months[month]["Related"]=0
    Months[month]["cases"]=0

#enter all tweets into the hashes 
for item in db:
    try:
        if db[item]["key"][2]==1:
            Months["January"]["Total"]+=1
            if db[item]["key"][3] in Dates["January"]:
                Dates["January"][db[item]["key"][3]]["Total"]+=1
                continue
            else:
                Dates["January"][db[item]["key"][3]]={}
                Dates["January"][db[item]["key"][3]]["Total"]=1
                Dates["January"][db[item]["key"][3]]["Related"]=0
                Dates["January"][db[item]["key"][3]]["Cases"]=0
                continue
        if db[item]["key"][2]==2:
            Months["February"]["Total"]+=1
            if db[item]["key"][3] in Dates["February"]:
                Dates["February"][db[item]["key"][3]]["Total"]+=1
                continue
            else:
                Dates["February"][db[item]["key"][3]]={}
                Dates["February"][db[item]["key"][3]]["Total"]=1
                Dates["February"][db[item]["key"][3]]["Related"]=0
                Dates["January"][db[item]["key"][3]]["Cases"]=0
                continue
        if db[item]["key"][2]==3:
            Months["March"]["Total"]+=1
            if db[item]["key"][3] in Dates["March"]:
                Dates["March"][db[item]["key"][3]]["Total"]+=1
                continue
            else:
                Dates["March"][db[item]["key"][3]]={}
                Dates["March"][db[item]["key"][3]]["Total"]=1
                Dates["March"][db[item]["key"][3]]["Related"]=0
                Dates["January"][db[item]["key"][3]]["Cases"]=0
                continue
    except:
        continue    

#searching each tweet for keywords or hashtags
keywords=["coronavirus","covid","virus","corona","quarantine","lockdown","socialdistancing","covid19","sarscov19","pandemic","isolation","wuhan","chinavirus"]
for item in db: 

        text = db[item]["doc"]["text"].lower()
        text = re.sub('[#@-_*&$!]','',text)
        for search in keywords:
            if re.search(search,text):
                if db[item]["key"][2]==1:
                    Months["January"]["Related"]+=1
                    Dates["January"][db[item]["key"][3]]["Related"]+=1
                    break
                if db[item]["key"][2]==2:
                    Months["February"]["Related"]+=1
                    Dates["February"][db[item]["key"][3]]["Related"]+=1
                    break
                if db[item]["key"][2]==3:
                    Months["March"]["Related"]+=1
                    Dates["March"][db[item]["key"][3]]["Related"]+=1
                    break

#entering cases into hash
for item in covid:
    if covid[item]["Month"]==1:
        try:
            Dates["January"][covid[item]["Day"]]["Cases"]=covid[item]["Cases"]
        except:
            continue
    if covid[item]["Month"]==2:
        try:
            Dates["February"][covid[item]["Day"]]["Cases"]=covid[item]["Cases"]
        except:
            continue
    if covid[item]["Month"]==3:
        try:
            Dates["March"][covid[item]["Day"]]["Cases"]=covid[item]["Cases"]
        except:
            continue
    

#print in table form
#print ("{:<5} {:<5} {:<5} {:<5} {:<5}".format("Day","Total","Related","Percent","Cases"))
#for month in Dates:
#    for i in range(1,31):
#        try:
#            print ("{:<5} {:<5} {:<7} {:<7} {:<6} {:<6}".format(month,i,Dates[month][i]["Total"], Dates[month][i]["Related"],'{0:.2f}'.format(Dates[month][i]["Related"]/Dates[month][i]["Total"]*100),Dates[month][i]["Cases"]))
#        except:
#            continue


#write to a csv file
FOut = open("data.csv","w")
header = "+\t%s\t%s\t%s\t%s\t%s\t%s" % ("Month","Day","Total", "Related","Percent","Cases")
print(header,file=FOut)
for month in Dates:
    for i in range(1,31):
        try:
            row = ">\t%s\t%s\t%s\t%s\t%s\t%s" % (month,i,Dates[month][i]["Total"], Dates[month][i]["Related"],'{0:.2f}'.format(Dates[month][i]["Related"]/Dates[month][i]["Total"]*100),Dates[month][i]["Cases"])
            print (row,file=FOut)
        except:
            continue
print("writing complete")

