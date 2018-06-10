from InstagramAPI import InstagramAPI #pip install PythonInstagram
import sys
import json
import requests
from requests import *
import os.path
#It doesn't have to be your account. It can be any, but if the profile you look is private, you need to follow it. 
API = InstagramAPI("USERNAME HERE", "PASSWORD HERE")
API.login()
lookupUser = input("\nUser for follower comparasion: ")
def getID(username):
	API.searchUsername(username)
	return API.LastJson['user']['pk']
def getFollowers(ID):
	followers = []
	followerDict = API.getTotalFollowers(ID)
	followerCount = len(followerDict)
	i = 0
	while i < followerCount:
		followers.append(followerDict[i]["username"])
		i += 1
	return followers
def writeToFile(followers):
	f = open(lookupUser + ".txt", "w")
	i = 0
	while i < len(followers):
		f.write(followers[i] + "\n")
		i += 1
	f.close()
	print("Wrote " + str(len(followers)) + " users to the file.")
def readFromFile(username):
	if os.path.isfile(username + ".txt"):
		oldfollowers = []
		try:
			f = open(username + ".txt", "r")
			fLines = f.readlines()
			for x in fLines:
				oldfollowers.append(x[:-1])
			return oldfollowers
		except:
			return False
	else:
		return False

oldFollowers = readFromFile(lookupUser)
curFollowers = getFollowers(getID(lookupUser))
if oldFollowers == False:
	writeToFile(getFollowers(getID(lookupUser)))
	print("This was the first time you searched for this user. You can now use comparing. ")
	exit()
mutualSet = set(oldFollowers) & set(curFollowers)
mutualList = []
print("\nThis account used to has " + str(len(oldFollowers)) + " followers.")
print("It now has " + str(len(curFollowers)) + " followers.")
writeToFile(curFollowers)
for i in mutualSet:
	mutualList.append(i)
i = 0
while i < len(mutualList):
	curFollowers.remove(mutualList[i])
	oldFollowers.remove(mutualList[i])
	i += 1
print("\nUnfollowed users: ")
i = 0
f = open(lookupUser + "_unfollowed.txt", "w")
try: 
	while i < len(oldFollowers):
		f.write(oldFollowers[i] + "\n")
		print(oldFollowers[i])
		i += 1
except: 
	pass
f.close()
i = 0
print("\nNew followers: ")
f = open(lookupUser + "_newFollowers.txt", "w")
try:
	while i < len(curFollowers):
		print(curFollowers[i])
		f.write(curFollowers[i] + "\n")
		i += 1
except: 
	pass
f.close()
