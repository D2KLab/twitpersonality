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
