
string = "Sun Mar 01 00:05:55 +0000 2020"
location = "sydney"

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
    return States[y]


