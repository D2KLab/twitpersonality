-TwitterDataExtraction
	Downloads tweets and friends ids (=profiles the users is following).
	If the number of users and the number of following is high, the script is very likely to timeout (15 minutes window).

-Tweets.py
	Downloads only tweets

Both the files require a single user name or the path to a file containing a list of usernames, one per line.
If a user is not found, the script moves to the nex one.

For authentication, the scripts read a file in the same directory that contains the credentials (access_token and access_token_secret).