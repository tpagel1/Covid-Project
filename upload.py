import json
import couchdb

user = "admin"
couch = couchdb.Server("http://%s:%s@172.26.128.126:5984/" % (user,"admin"))
db = couch["mydb"]
small =couch.create("small")
'''
user = "admin"
couch = couchdb.Server("http://%s:%s@127.0.0.1:5984/" % (user,12345))
db = couch.create("covidjanmarch")
with open ("nswcovidmarch.json", encoding="utf8") as f:
    data = json.load(f)
    for i in data:
        db.save(i)
'''

#for item in db:
#    print(db[item]['doc']['entities']

for item in db:
    data={}
    data["file"]=item
    print(data)
    small.save(data["file"])
