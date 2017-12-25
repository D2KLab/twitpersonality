User Personality Prediction
======
Once we have trained a machine learning model, we can use it to predict the personality of a new user. To do this, we use twitter data that we collected in the first part of the application (see <tt>DataExtraction</tt>). 
Depending on the wealth of data we were able to build the model on, we may use tweets plus additional information such as demographics or network properties.

Description
-----
Tweets are stored in a text file inside a folder with the same name as the username of the person whose personality we are trying to predict.
We read them, and apply the same transformations used to feed data to the algorithm, namely:
* <b>Preprocessing</b> Includes transformation to lowercase, stopwrods and punctuation removal, tokenization.
* <b>Embeddings</b> Resulting tokens are transformed into embeddings the same way it is done for the training phase. One method among sum, max, min, average, concatenation is chosen.

Tweet-Wise vs User-Wise
-----
Two approaches are possible
* <b>Tweet-wise</b> Each tweet is transformed in embedding and a personality is predicted from it. The final personality scores will be computer as the mean of the scores of each tweet.
* <b>User-Wise</b> Embeddings representations of tweets are merged together by computing the mean, so that we have only one vector for each user, giving us the personality score.

Both option will be tested in terms of accuracy and error.
