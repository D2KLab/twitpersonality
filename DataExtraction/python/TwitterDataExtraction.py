import tweepy
import pyperclip
import os
import time
import sys
from pathlib import Path
from datetime import datetime

#print (str(datetime.time(datetime.now())))

#create the root folder if not exists
if not os.path.exists("Data"):
    os.makedirs("Data")

twitterAuthData = Path("twitterAccess.txt")

if not twitterAuthData.is_file() or os.stat("twitterAccess.txt").st_size == 0:
	#no previous authentication data, need to autenthicate via browser
	auth = tweepy.OAuthHandler("Bo0Usm7MbQLJGTUv3jAuwY1qz", "hx0gsX49KIDsm1MgWFuuYOV1zrR06Tcz5r06RmMxn4SsR41dFr")

	try:
	    redirect_url = auth.get_authorization_url()
	    print("Redirect url:", redirect_url)
	    #copy redirect url in clipboard
	    pyperclip.copy(redirect_url)
	except tweepy.TweepError:
	    print ('Error! Failed to get request token.')

	verifier = input('Verifier:')

	try:
	    auth.get_access_token(verifier)
	except tweepy.TweepError:
	    print ('Error! Failed to get access token.')

	access_token = auth.access_token
	access_token_secret = auth.access_token_secret

	twitterAuthData = open("twitterAccess.txt", "w")
	twitterAuthData.write(auth.access_token+"\n"+auth.access_token_secret);
	twitterAuthData.close();
else:
	#already got auth data, read it from file
	twitterAuthData = open("twitterAccess.txt", "r")
	access_token = twitterAuthData.readline()[:-1] #exclude line feed from token string
	access_token_secret = twitterAuthData.readline()
	twitterAuthData.close()

auth = tweepy.OAuthHandler("Bo0Usm7MbQLJGTUv3jAuwY1qz", "hx0gsX49KIDsm1MgWFuuYOV1zrR06Tcz5r06RmMxn4SsR41dFr")
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

usernames = []
search_input = input("enter username or filename:")
if not Path(search_input).is_file():
	#entered username
	usernames.append(search_input)
else:
	#entered file name
	if os.stat(Path(search_input)).st_size == 0:
		sys.exit("Error. File is empty.")
	for name in open(search_input, "r"):
		usernames.append(name[:-1])

for username in usernames:
	#retrieve user profile
	print("USERNAME: ", username)

	error = 0

	try:
		user = api.get_user(username) #access fields with user.[field_name]		
	except tweepy.TweepError as err:
		print("An error has Occurred.", err, sep="\n")
		continue

	dir_name = os.path.join("Data",username)
	if not os.path.exists(dir_name):
		os.makedirs(dir_name)
	fp = open(dir_name+"/"+username+".txt", "w+")
	#write user data in file
	fp.close()

	#get tweets
	tweets = []
	try:
		for page in tweepy.Cursor(api.user_timeline, username, count=200).pages():
		    for tweet in page:
		    	tweets.append(tweet.text)
	except tweepy.TweepError as err:
		print("An error has Occurred.", err, sep="\n")


	fp = open(dir_name+"/"+username+"_tweets.txt", "wb")
	for tweet in tweets:
		fp.write((tweet+"\n\n").encode("utf-8"))
	fp.close()

	#read user friends
	#	if frends < 200 -> read them using api.friends(username, count=200)
	#	else use api.friends_ids(username) which returns up to 5000
	friends_names = []
	friends_ids = []
	if user.friends_count < 200:
			try:
				friends = api.friends(username, count = 200)
				for friend in friends:
					friends_names.append(friend.name)
					friends_ids.append(friend.id)
			except tweepy.TweepError as err:
				print("An error has Occurred While retrieving freinds names.", err, sep="\n")
	else:
		#first get the ids (max 900 every 15 minutes)
		try:
			for ids_chunk in tweepy.Cursor(api.friends_ids, username).pages():
				friends_ids.extend(ids_chunk)
		except tweepy.TweepError as err:
			print("An error has Occurred while retrieving ids.", err, sep="\n")

		for user_id in friends_ids:
			try:
				name = api.get_user(user_id).name
				friends_names.append(name)
			except tweepy.TweepError as err:
				print("An error has Occurred while retrieving user with id "+user_id, err, sep="\n")
				continue

	i=0
	fp = open(dir_name+"/"+username+"_friends.txt", "wb")
	while i < len(friends_names):
		fp.write((str(friends_ids[i])+"\t"+friends_names[i]+"\n").encode("utf-8"))
		i+=1
	fp.close()

	print("user tweets:",len(tweets))
	print("user friends:", len(friends_names))

	input()
