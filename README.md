Computing personality traits from tweets using word embeddings and supervised learning
======

Online Social Network (OSNs) are a place where users can chat, make new friendships, explore, share or create digital content. The most popular among these platforms in terms of number of users is surely Facebook, followed by Twitter, Instagram, Youtube, and many more. Every action carried out in one on these platforms leaves a digital footprint that can be analyzed to gain an insight about preferences and behavioural patterns of individuals. There is an excellent body of work in the literature about computing personality traits of users from the information they reveal on Social Media, whether it is done on purpose (i.e. Facebook likes, Twitter follows) or not, such as textual features used in status updates/tweets. The latter motivates our study. We propose a supervised learning approach to compute personality dimensions by only relying on what an individual tweets about his thoughts. The approach segments tweets in tokens, then it learns word vector representations as distributed embeddings which are then used to feed a supervised learner classifier. We demonstrate the feasibility and the effectiveness of the approach by measuring the precision tested against an international benchmark.
We also show how inferring personality from Social Media could be useful for a Recommender System, personalizing a number of offers (i.e. tourist/musical) based on the individual's specific traits.

The application will be structured in the following sections:

Training and Tuning
-----
First of all, we need to derive a machine learning algorithm that is able to compute personality traits from text. Our Gold Standard is MyPersonality dataset containing nearly 10.000 status updates of 250 users, annotated with their personality traits on a scale 0-5 [1]. Different algorithms and configurations are tested, and their overall performance is evaluated using an error metric, such as MSE. It should be noted that we train and tune a different model for each personality trait.
Each status update is preprocessed to obtain a list of tokens, then the textual information is converted into a distributed representation in the vector space, using word embeddings. We choose to use a pre-trained model from FastText rather than training our own. We explore different techniques for transforming statuses into embeddings and for feeding them to the algorithm.

[1] Celli F., Pianesi F., Stillwell D., Kosinski M. (2013) Workshop on Computational Personality Recognition (Shared Task). In Proceedings of WCPR13, in conjunction with ICWSM-13.

Personality Prediction
-----
Once the training of the algorithm is completed, we can test it with a new individual.
To download an individual's tweets, we query Twitter's REST API at the endpoint <i>statuses/user_timeline</i>. This returns up to 200 tweets from the user we specify as parameter. We process tweets the same way as for training the algorithm, and feeding them to the model it returns the personality traits of the individual.

Recommendation
-----
Personality has been shown to correlate to user preferences. This includes music and movies taste, marketing brands, voting preference or even favorite pets. Knowing an individual's personality then makes it possible to offer a unique and personalized experience to users based on their preferences.
We show how a musical and a tourist recommender system would benefit from this piece of information.
