from InstagramAPI import InstagramAPI #https://github.com/raphasousa/Instagram-API-python clone this. 
import sys			      #Install requirements with pip3 install -r requirements.txt
import json		 	      #Change the InstagramAPI.py file that you cloned with this: 
import requests			      #https://github.com/raphasousa/Instagram-API-python/blob/f1418b6fe7eba04636a26a40740b007943d845a7/InstagramAPI/InstagramAPI.py
from requests import *		      #Then run python setup.py install
import os.path
import time

API = InstagramAPI("UsernameOfBot", "PasswordOfBot") 
API.login()
def getID(username):
	API.searchUsername(username)
	return API.LastJson['user']['pk']
def getJson(ID):
	url = "https://i.instagram.com/api/v1/users/" + str(ID) + "/info/"
	request = requests.get(url)
	return request.json()
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
lookupUsers = ["inf_dragonfly", "mrdm47", "g._ucar"] #Bot will send users in this list who unfollowed/followed them.
while 1: 
	for lookupUser in lookupUsers:
		print(lookupUser)
		sendString = ""
		lookupID = getID(lookupUser)
		oldFollowers = readFromFile(lookupUser)
		curFollowers = getFollowers(lookupID)
		if oldFollowers == False:
			writeToFile(getFollowers(lookupID))
			print("This was the first time you searched for this user. You can now use comparing. ")
			continue
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
		sendString = sendString + "Users who have unfollowed: \n" #
		i = 0
		f = open(lookupUser + "_unfollowed.txt", "w")
		try: 
			while i < len(oldFollowers):
				f.write(oldFollowers[i] + "\n")
				sendString = sendString + oldFollowers[i] + + ", "
				print(oldFollowers[i])
				i += 1
		except: 
			pass
		f.close()
		i = 0
		print("\nNew followers: ")
		sendString = sendString + "\nUsers who have followed: \n"
		f = open(lookupUser + "_newFollowers.txt", "w")
		try:
			while i < len(curFollowers):
				print(curFollowers[i])
				f.write(curFollowers[i] + "\n")
				sendString = sendString + curFollowers[i] + ", "
				i += 1
		except:
			pass
		x = API.direct_message(sendString, lookupID)
		print(sendString)
		print(x)
		f.close()
	time.sleep(60 * 60 * 24) #Wait for 24 hours.
	
