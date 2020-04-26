# reddit-flair-detector

A Reddit Flair Detector web application to detect flairs of India subreddit posts using Machine Learning algorithms. The application can be found live at [Reddit Flair Detector](https://redditherokup.herokuapp.com/). <br>

### Directory Structure
data_scrapping_and_cleaning is the code to collect data.<br>
EDA is the data analysis. <br>
flair_Detector_ml_baselines contatins the ml baselines. <br>
bert contains all the bert codes. (train, preprocess) <br>

### django app
reddit_flair contains django code for website. To run, install the requirements and execute `python manage.py runserver`

### Main libraries used
  1. [praw]
  2. [scikit-learn]
  3. [Django]
  4. [pandas]
  5. [numpy]
  6. [pytorch]
  
### ML Approach

The approach taken for the task is as follows:

  1. Collect 100 India subreddit data for each of the 12 flairs using `praw` module [[1]](http://www.storybench.org/how-to-scrape-reddit-with-python/).
  2. The data includes *title, comments, body, url, author, score, id, time-created* and *number of comments*.
  3. For **comments**, only 20 top level comments are considered in dataset and no sub-comments are present.
  4. The ***title, comments*** and ***body*** are cleaned by removing bad symbols.
  5. four types of features are considered for the the given task:
    
    a) Title
    b) Comments
    c) Body
    d) Combining Title, Comments and Body as one feature.
  6. The dataset is split into **80% train** and **20% test** data using `train-test-split` of `scikit-learn`.
  7. The dataset is then converted into a `Vector` and `TF-IDF` form.
  8. Then, the following ML BASELINE ALGORITHMS (using `scikit-learn` libraries) are applied on the dataset:
    
    a) Logistic Regression
    b) Random Forest
    c) LinearSVC
   9. Training and Testing on the dataset showed the **Random Forest** showed the best testing accuracy of **74.3%** when trained on the combination of **Title + Comments + BODY** feature.
   10. The best model is saved and is used for prediction of the flair from the URL of the post.
    
### BERT approach
1. The The features **Title + Comments + BODY** are truncated to 700 length (as found out from the EDA).
2. They are given to `bert-base-uncased` (which is used as a feature extractor). This layer is not fintuned.
3. The output of bert is given to an attention layer to compute relative importance of words.
4. The attention output is fed to dense layers for dimensionality reduction.
5. The final dense layer uses softmax and classifies into classes.
6. This model was run only for 24 epochs.
7. This method performed poorly as compared to ML due to lack of computation resources and data. However it can be improved by adding more data and runnig for more epochs. 
