#!/usr/bin/env python
from mpi4py import MPI
import numpy as np
import json
import datetime

start_time=datetime.datetime.now()


comm = MPI.COMM_WORLD
size=comm.Get_size()
rank=comm.Get_rank()

with open("bigTwitter.json","r",encoding='utf-8') as f:
	partition=[]
	i=1
	for line in f:
		if i%size==rank:
			try:
				entry={}
				data=json.loads(line[:-2])
				entry["id"]=data["id"]
				temphashtags=data["doc"]["entities"]["hashtags"]
				tempcontainer=[]
				for item in temphashtags:
					tempcontainer.append(item["text"].lower())
				entry["hashtags"]=tempcontainer
				entry["language"]=data["doc"]["lang"]
				if tempcontainer!=[]:
					partition.append(entry)
					i=i+1
				else:
					i=i+1
					continue	
			except:
				i=i+1
				continue
		else:
			i=i+1
			continue
totalhashtags={}
totallanguages={}
for item in partition:
	for hashtags in item["hashtags"]:
		if hashtags in totalhashtags:
			totalhashtags[hashtags]=totalhashtags[hashtags]+1
		else:
			totalhashtags[hashtags]=1
	lang=item["language"]
	if lang in totallanguages:
		totallanguages[lang]=totallanguages[lang]+1
	else:
		totallanguages[lang]=1
resultset=[totalhashtags,totallanguages]
totalresults=comm.gather(resultset)

if rank==0:
	finalhash={}
	finallang={}
	for entry in totalresults:
		for item in entry[0].keys():
			if item in finalhash.keys():
				finalhash[item]=finalhash[item]+entry[0][item]
			else:
				finalhash[item]=entry[0][item]
		for item in entry[1].keys():
			if item in finallang.keys():
				finallang[item]=finallang[item]+entry[1][item]
			else:
				finallang[item]=entry[1][item]
	print("The top 10 hashtags are:")
	j=0
	for w in sorted(finalhash,key=finalhash.get,reverse=True):
		if j<10:
			try:
				print(w,finalhash[w])
				j=j+1
			except:
				print("could not print this hashtag as it contains non-ascii")
		else:
			break
	print("\nThe top 10 languages are:")
	k=0
	for w in sorted(finallang,key=finallang.get,reverse=True):
		if k<10:
			if w!="und":
				print(w,finallang[w])
				k=k+1
			else:
				print("this language was {}, which doesn't count. It had a count of {} though.".format(w,str(finallang[w])))
				continue
		else:
			break

	end_time=datetime.datetime.now()
	timediff = end_time-start_time
	print("\nTotal time taken is {} seconds, and {} microseconds".format(timediff.seconds,timediff.microseconds))
