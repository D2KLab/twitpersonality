Parameters' tuning for Machine Learning Models
======
Python3 scripts to test machine learning models with different parameters and measure their accuracy.
This guide refers to the following scripts:

* **Tuning_SVM.py**
* **Tuning_LASSO.py**

We also report in this repository other scripts that may be useful for training and testing the models. <tt>Tuning_SVM_OCEAN.py</tt> and <tt>Tuning_LASSO_OCEAN.py</tt> are just extensions of the formers.

We remark with particular importance the script <tt>Train_SVM_models.py</tt> which we used to train the five final SVM models used for testing the approach on Twitter.

<tt>Train_SVM_models_Big.py</tt> and <tt>Train_SVM_models_Big_UserWise.py</tt> are used to train the five predictive SVM models on myPersonality big dataset, that is the one composed by 23 million status updates, whose employment and relative results are not reported in the paper. Finally, <tt>Train_SVM_models_Twitter.py</tt> uses the Twitter Gold Standard as a training set for the SVM models. That is useful to test the effectiveness of our approach when transfer learning is not applied.

Requires
-----
* <tt>datasetUtils.py</tt>
* <tt>embeddings.py</tt>
* numpy
* pandas
* scipy
* scikit-learn

File References
-----
* <tt>datasetUtils.py</tt> and <tt>embeddings.py</tt> must be in the same directory as tuning files.
* Embeddings datasets (fasttext and dataset9) <b>should</b> be in the same directory ad tuning files.
* MyPersonality dataset must be in <tt>Dataset/</tt> folder.

Description
-----
For simplicity, it is provided a bash script <tt>extensiveTuning.sh</tt> that handles all the required programs' launches. It can be found in <tt>twitpersonality/Utilities</tt>.

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

Post-Wise vs User-Wise
-----
How should we treat different status updates from the same user ?
* <b>Post-Wise</b> Each post is converted into embedding and is treated as a record for training the algorithm.
* <b>User-Wise</b> Embeddings of posts for the same user are averaged. The resulting vector is a record for the algorithm.

We tested both the approaches, and the first one seems to be more effective. This is probably because when averaging all the posts of a user into a single one we lose many subtle manifestations of personality by flattening them to their median value, hence the model tends to predict average values and is less discriminative.

Usage
-----

### Shell Script
```
extensiveTuning.sh
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
For each machine learning techinque and for each BIG 5 trait, the shell script will output two text files, a <tt>.csv</tt> and a <tt>.txt</tt>.
The csv file stores the mean over the 10 cross-validation of the 3 accuracy measures for each combination of the configuration paramenters, while the txt contains the PCC score and relative p-value for each cross-validation iteration and combination.

SVM:
* <tt>Tuning_SVM_<BIG5>_<embeddings_dataset>_<shuffle/noShuffle>.csv</tt> 
* <tt>Tuning_SVM_<BIG5>_<embeddings_dataset>_<shuffle/noShuffle>_pcc.txt</tt>

LASSO:
* <tt>Tuning_LASSO_<BIG5>_<embeddings_dataset>_<shuffle/noShuffle>.csv</tt>
* <tt>Tuning_LASSO_<BIG5>_<embeddings_dataset>_<shuffle/noShuffle>_pcc.txt</tt>
 
files are stored in a folder <tt>Results/</tt> created at execution time.

Adding everithing up: Training, Tuning, and saving models to file system
-----
For simplicity, we report a use case scenario which allows to replicate our experiment from start to end. Once done, the result of this pipeline are five machine learning models that can be used to predict the personality of new users. If you already have trained your models and are only interested in predicting personality from tweets, please refer to Section <tt>twitpersonality/Test/</tt>.

First, we launch the tuning phase by executing either <tt>extensiveTuning.sh</tt> or <tt>extensiveTuning_OCEAN.sh</tt>. Those script can be found under <tt>twitpersonality/Utilities/</tt>, and provide different output. The first creates two files for each personality trait (O,C,E,A,N) and for each algorithm (LASSO, SVM), while the second only creates two files for each algorithm. Those two files, in both cases, store mean squared error and Pearson correlation coefficient about the 10-fold cross-validation. We choose to compute pcc because it is a useful measure of the relationship between actual and predicted values.

When the tuning phase has completed, we analyze the results stored in the output files to seek the algorithm configuration that performed the best on the training data. The metric for choosing such configuration may vary, for example we want the lowest MSE overall or the average lowest MSE for the five traits. 

Once we select the algorithm and configuration that best suit our case, we can finally train the predictive models. This can be done using <tt>Train_SVM_models.py</tt>. The script trains 5 SVM models on the whole dataset from the Gold Standard, without performing cross-validation, and saves those models on disk. We did not implement a similar techique for LASSO, since tuning results show that SVM performs better for our case.

After training the models, we can move to the <tt>twitpersonality/Test/</tt> phase.

