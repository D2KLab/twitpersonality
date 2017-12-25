Data Extraction from Twitter
======

* *This section is under development* *

The first part of the project consists in extracting public user data available on Twitter. We are interested in tweets, number of followers/following, and basic demographic information.

A first prototype was written in PHP using <tt>twitteroauth</tt> library, but the final application will be written in Python 3 with <tt>tweepy</tt> library.

Description
-----
The script expects one of the following as input:

* Twitter username
* Local text file with one or more Twitter usernames, one per line

For each one of the provided usernames, the script first checks if someone with that name exists in the twitter database; if so, it retrieves basic profile information (which includes followers/following) and tweets. It is also possible to get the lists of followers/following, to compute for example some network statistics, but be careful with API rate limits.

API Endpoints
-----
* <tt>GET users/show.json?screen_name=username</tt> (limit = 900) Returns basic profile information.
* <tt>GET statuses/user_timeline?screen_name=username&count=200</tt> (limit = 1500) Returns latest 200 user tweets.
* <tt>friends/ids.json?screen_name=username</tt> (limit = 15) Returns up to 5000 following ids. To get usernames, next call is required.
* <tt>users/show.json?user_id =id</tt> (limit = 900) Returns the same response as the first call.
* <tt>/friends/list</tt> (limit = 15) Returns up to 200 following usernames.

All temporal windows for API limits are 15 minutes long. <tt>tweepy</tt> automatically handles timeout by waiting for that amount a time when a timeout occurs.
