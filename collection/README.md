Data Extraction from Twitter
======

The first part of the project consists in extracting public user data available on Twitter. We are interested in tweets, number of followers/following, and basic demographic information.

Description
-----
Twitter data can be downloaded using one of the two scripts:

* **TwitterDataExtraction.py** Downloads all the tweets and all the names and ids of the Twitter friends (= profiles being followed by the user) of the specified user(s). Please note that this script is very likely to reach the API rate limit and timeout (15 minutes window).
* **Tweets.py** Downloads only the tweets of the specified user(s). It only risks to timeout when the number of users is very high, in the order of hundreds or more.

The scripts expect one of the following as input:

* Twitter username
* Local text file with one or more Twitter usernames, one per line

For each one of the provided usernames, the scripts first check if someone with that name exists in the twitter database; if so, they retrieve basic profile information (which includes number of followers/following) and tweets. It is also possible to get the lists of followers/following, to compute for example some network statistics, but be careful with API rate limits.

Collected data is saved locally, a new folder is created for each user, inside of which are two text files, one for profile information and the other for tweets. These files will be used to determine the personality of the users, according the Five Factor model. For more information, see <tt>Test</tt>.


Authentication
-----
<tt>Tweepy</tt> implements standard OAuth authentication. Both the scripts require valid authentication data to be stored in a file called **twitterAccess.txt**. The file must store the access token on the first line and the access token secret on the second line.

For more information about obtaining access token refer to [Twitter Documentation](https://developer.twitter.com/en/docs/basics/authentication/overview/oauth) and [Tweepy documentation](http://tweepy.readthedocs.io/en/v3.5.0/auth_tutorial.html).


API Endpoints
-----
* <tt>GET users/show.json?screen_name=username</tt> (limit = 900) Returns basic profile information.
* <tt>GET statuses/user_timeline?screen_name=username&count=200</tt> (limit = 1500) Returns latest 200 user tweets.
* <tt>friends/ids.json?screen_name=username</tt> (limit = 15) Returns up to 5000 following ids. To get usernames, next call is required.
* <tt>users/show.json?user_id =id</tt> (limit = 900) Returns the same response as the first call.
* <tt>/friends/list</tt> (limit = 15) Returns up to 200 following usernames.

All temporal windows for API limits are 15 minutes long. <tt>tweepy</tt> automatically handles timeout by waiting for that amount of time when a timeout occurs.
