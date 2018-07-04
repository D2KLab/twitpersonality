import tweepy
import os
import sys
from pathlib import Path
import json
import re

#create the root folder if not exists
if not os.path.exists("Data"):
    os.makedirs("Data")

twitterAuthData = Path("twitterAccess.txt")

if not twitterAuthData.is_file() or os.stat("twitterAccess.txt").st_size == 0:
	#no previous authentication data, need to autenthicate via browser
	auth = tweepy.OAuthHandler("<your_consumer_api>", "<your_consumer_secret>")

	try:
	    redirect_url = auth.get_authorization_url()
	    print("Redirect url:", redirect_url)
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
	twitterAuthData.write(auth.access_token+"\n"+auth.access_token_secret)
	twitterAuthData.close()
else:
	#already got auth data, read it from file
	twitterAuthData = open("twitterAccess.txt", "r")
	access_token = twitterAuthData.readline().rstrip()#[:-1] #exclude line feed from token string
	access_token_secret = twitterAuthData.readline()
	twitterAuthData.close()

print(access_token+ "\n" + access_token_secret)

auth = tweepy.OAuthHandler(access_token, access_token_secret)
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

	with open(dir_name+'/'+username+'.json', 'w') as outfile:
		json.dump(user._json, outfile)

	#get tweets
	tweets = []
	i = 0
	try:
		for page in tweepy.Cursor(api.user_timeline, username, count=200).pages():
		    for tweet in page:

		    	if re.match(r'^(RT)',tweet.text):
		    		#ignore pure retweets (= with no associated text)
		    		continue

		    	tweet_text = re.sub(r'\n'," ", tweet.text)
		    	tweets.append(tweet_text)
		    	i += 1
	except tweepy.TweepError as err:
		print("An error has Occurred.", err, sep="\n")

	print("Done! User tweets:",len(tweets))

	fp = open(dir_name+"/"+username+"_tweets.txt", "wb")
	for tweet in tweets:
		fp.write((tweet+"\n").encode("utf-8"))
	fp.close()
