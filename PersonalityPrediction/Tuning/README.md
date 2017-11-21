Parameters' tuning for Machine Learning Models
======
Python3 scripts to test machine learning models with different parameters and measure their accuracy

Requires
-----
* <tt>datasetUtils.py</tt>
* <tt>embeddings.py</tt>
* numpy
* scipy
* scikit-learn

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

While for LASSO, we used the following values of <tt>alpha</tt>:
```
alpha_lasso = [1e-15, 1e-10, 1e-8, 1e-5, 1e-4, 1e-3, 1e-2, 1, 5, 10]
```

For estimating the accuracy, we used three different measures:
 * <b>Mean Squared Error</b>
 * <b>Coefficient of Determination (R2)</b>
 * <b>Pearson Correlation Coefficient</b> between actual and predicted values
 
All the measures are calculated using 10-fold cross-validation.

Usage
-----

### Shell Script
```
extensiveTuning_OCEAN.sh
```
### Manual execution
For <tt>Tuning_LASSO.py</tt> <tt>and Tuning_SVM.py</tt>:
```
python <script_name> <BIG5_trait> <embeddings_dataset> <dataset_path> <shuffle_data>
```
For <tt>Tuning_LASSO_OCEAN.py</tt> <tt>and Tuning_SVM_OCEAN.py</tt>:
```
python <script_name> <BIG5_trait> <embeddings_dataset> <dataset_path> <shuffle_data>
```

Where:
* <b>BIG5_trait</b> <tt>O C E A N o c e a n</tt>
* <b>embeddings_dataset</b> <tt>fasttext dataset9</tt>
* <b>dataset_path</b> <tt>path/to/the/file</tt>
* <b>shuffle_data</b> <tt>True False yes no</tt>


Output
-----
For each machine learning techinque, the shell script will output two text files, a <tt>.csv</tt> and a <tt>.txt</tt>.
The csv file stores the mean over the 10 cross-validation of the 3 accuracy measures for each combination of the configuration paramenters, while the txt contains the PCC score and relative p-value for each cross-validation iteration and combination.

SVM:
* <tt>Tuning_SVM_<embeddings_dataset>_<shuffle/noShuffle>.csv</tt> 
* <tt>Tuning_SVM_<embeddings_dataset>_<shuffle/noShuffle>_pcc.txt</tt>

LASSO:
* <tt>Tuning_LASSO_<embeddings_dataset>_<shuffle/noShuffle>.csv</tt>
* <tt>Tuning_LASSO_<embeddings_dataset>_<shuffle/noShuffle>_pcc.txt</tt>
 
files are stored in a folder <tt>Results/</tt> created at execution time.
