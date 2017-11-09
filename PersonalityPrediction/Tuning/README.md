Parameters' tuning for Machine Learning Models
======
Python 3 scripts to test machine learning models with different parameters and measure their accuracy

Description
-----
For simplicity, it is provided a bash script <tt>extensiveTuning_OCEAN.sh</tt> that handles all the required programs' launches.

The script tests two different Machine Learning techniques: LASSO and Support Vector Machines.
Moreover, for each of the two mentioned techniques, the following method for computing word embeddings of a post are tested:
  * <b>Sum</b> the sum of all word embeddings, element-wise
  * <b>Max</b> for each element, the maximum among all the words
  * <b>Min</b> for each element, the minimum among all the words
  * <b>Average</b> element-wise average of all word embeddings
  * <b>Concatenation</b> of max, min and average, in this order
  
For the word embeddings, we used a pre-trained model from FastText, available at: https://fasttext.cc/docs/en/english-vectors.html (<tt>wiki-news-300d-1M.vec.zip</tt>).

For SVM, these are the configuration paraters tested:
```
kernel = linear, rbf, poly
gamma = 0.01, 0.1, 1, 10
C = 1, 10, 100, 1000
degree = 2, 3
```
All the significant combinations are tested (es. <tt>degree</tt> is only significant when using a <tt>poly</tt> kernel), except for <tt>linear</tt> kernel which was tested only with <tt>C=1</tt>.
  
  
  

```
extensiveTuning_OCEAN.sh
```
