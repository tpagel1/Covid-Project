import couchdb
user = "admin"
couch = couchdb.Server("http://%s:%s@127.0.0.1:5984/" % (user,12345))
db = couch["project2"]

for item in db:
    print(db[item])
    #print(db[item]['doc'])
    #print(db[item]['doc']['entities'])