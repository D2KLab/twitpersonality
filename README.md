<h1>personalized-marketing</h1>
The goal of this project is developing an application that can create personalized marketing offers, based on the information that can be automatically gathered from online social networks, namely Facebook, Twitter, and LinkedIn.
The application will be composed of three main parts.

#

<h3>1 - Data Extracion from Social Networks</h3>
In this part we develop a web application that is able to extract specific data from the websites listed above. Data is collected automatically and stored in a proper way for further use.
Specifically, information we are looking for is demographics (such as gender, age range) and page likes/follows.

#

<h3>2 - Personality Prediction</h3>
Using data collected in the previous step, we want to predict the user's personality, according to the well-estabilished Five Factor Model. This model describes someone's personality using 5 measures (Openness, Conscientiousness, Extroversion, Agreeableness, Neuroticism) and assigning a score to each of them. In order to make the prediction, we use a machine learning algorithm and train it on a dataset od users.

#

<h3>3 - Recommendation</h3>
Once we have constructed a user profile, we can use it to make the personalized marketing recommendation. We use a marketing dataset comtaining a list of items and we select from it the one(s) that have the highest match with the user profile.
