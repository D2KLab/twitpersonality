Social Media Profiling to Driving Products Recommendations
======

The goal of this project is to develop an application that can create personalized items or media offers, such as a particular phone brand or movie rather than another, based on the information that can be automatically gathered from Twitter. We chose to use Twitter because we want to work with public users' data, namely tweets.

The application will be composed of three main parts.

Data Extracion from Twitter
-----
WIth a registered Twitter application, for each person in our user base, we retrieve all tweets plus some basic demographic and network information of that user. 

Personality Prediction
-----
Using data collected in the previous step, we want to predict the user's personality, according to the well-estabilished Five Factor Model. This model describes someone's personality using 5 measures (Openness, Conscientiousness, Extroversion, Agreeableness, Neuroticism) and assigning a score to each of them. 
To make the prediction, we use train a machine learning algorithm on a dataset of users. The best algorithm and its configuration are selected after testing different cadidates.

More details in <tt>PersonalityPrediction</tt> folder.

Recommendation
-----
Once we have personality scores of a user, we can use them in a Recommender System, selecting the best item/media match(es) for that user.
