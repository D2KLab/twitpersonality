User Personality Prediction
======
Once we have trained a machine learning model, we can use it to predict the personality of a new user. To do this, we use twitter data that we collected in the first part of the application (see <tt>Collection</tt>). 
Depending on the wealth of data we were able to build the model on, we may use tweets plus additional information such as demographics or network properties.

Description
-----
Tweets are stored in a text file inside a folder with the same name as the username of the person whose personality we are trying to predict.
We read them, and in addition to the same transformations used to feed data to the algorithm, we also apply some clenaing steps specific for tweets:

* <b>Cleaning</b> We remove retweets, URLs and mentions.
* <b>Preprocessing</b> Includes transformation to lowercase, stopwrods and punctuation removal, tokenization.
* <b>Embeddings</b> Resulting tokens are transformed into embeddings the same way it is done for the training phase. One method among sum, max, min, average, concatenation is chosen. 

Tweet-Wise vs User-Wise
-----
Two approaches are possible
* <b>Tweet-Wise</b> Each tweet is transformed in embedding and a personality is predicted from it. The final personality scores will be computer as the mean of the scores of each tweet.
* <b>User-Wise</b> Embeddings representations of tweets are merged together by computing the mean, so that we have only one vector for each user, giving us the personality score.

Tweet-Wise approach is implemented in <tt>predict-personality1.py</tt> while User-Wise is implemented in <tt>predict-personality2.py</tt>. We tested both the approaches for our experiment, and we observed that the first one is more effective. The results reported in the paper only refer to that one.


MyPersonality Big
-----
We also report the scripts used to test the models trained on myPersonality Big. They are not so different from the ones based on myPersonality small, the only difference rly in the predictive models that are loaded at runtime.


Evaluating the quality of the predictions
-----
<tt>twitusers_benchmark.py</tt> and <tt>plot_tweets_predictions.py</tt> are two utility scripts used to compare the predicted personality traits with the ground-truth labels derived from questionnaires. The first computes mean squared error and stores it in a file called <tt>twitusers_predictions_benchmark.csv</tt>; the latter plots the predicted values against the true values while at the same time storing the mean squared error in <tt>twitusers_predictions_benchmark_smallBig.csv</tt>.

Usage example
-----
In order to make the experiment easier to replicate, we report an example of using the models to predict personality of unknown users and evaluating the accuracy.

### Requirements:
* A file containing the ground truth values of users' personality scores (<tt>questionnaires.csv</tt>).
* A collection of tweets for one or more users, stored in <tt>/Data/<username>/<username>_tweets.txt</tt>.

We launch <tt>predict_personality1.py</tt> and specify either a username or a filename containing a list of usernames, one per line. For each user, the script performs the following operations on his tweets (in this order): cleaning, preprocessing, vector space transformation.
Vector representation of tweets are fed to the machine learning models that compute a personality score for each one of the BIG 5 trait, and are saved in <tt>personality_predictions1.csv</tt> under the same directory.
To compute the MSE over the predicted values, we execute <tt>twitusers_benchmark.py</tt> which reads both <tt>questionnaires.csv</tt> and <tt>personality_predictions1.csv</tt>, and compares the values for each user and for each trait. Mean squared error values are stored in <tt>twitusers_predictions_benchmark.csv</tt>.
