## ByRatings assignment
**Author:** Guillem Sala Fernandez
### The challenge
The problem consists of the analysis of an anonymized dataset from an E-commerce transactional database as well as the creation of a predictive model.

The candidate is expected to perform an exploratory analysis of the dataset and to develop a model to predict the quarterly monetary value of each user. More specifically, given a date (present) the model should estimate the aggregated billing of all the purchases each user will make during the following 90 days. Think also about how this model could help to improve business KPIs.

The problem statement is opened on purpose since one of the objectives of this challenge is to evaluate how a problem like this is faced. Regarding the predictive model, the goal is not to build a very complex model to achieve awesome accuracy. This is not a Kaggle competition. We prefer easier models that work well enough and you can explain and justify very well. We are particularly interested in the approach to modelize the problem and evaluate the predictive performance of your solution.

The analysis can be done either in Python or R, although the first is preferred. The results can be presented in any friendly format (Jupyter, R markdown, slides…). Whenever possible, show plots and tables that support your conclusions.

#### Key points:
[X] Exploratory analysis

[X] Design of the training and evaluation procedures to build the predictive model 

[X] ETL and feature engineering to build the tables that will be used as input to the predictive model

[X] Implementation in a production scenario

[X] Performance evaluation metrics and baselines to be considered

[X] Business case

The provided dataset includes two tables:
- User table (“sds_users.csv”): All the information contained in this table is generated when the users are registered/created.
  - user_id: Unique user identifier
  - created_at: User creation/registration timestamp
  - birthyear: User birth year
  - gender: User gender
  - is_active: User activity flag (inactive users can also place orders)
  - maildomain: User email domain (code)
  - region: User region (code)
  - orig_1: User origin 1 (code)
  - orig_2: User origin 2 (code)
  - utm_src: UTM source when the user was registered (code)
  - utm_med: UTM medium when the user was registered (code)
  - utm_cpg: UTM campaign when the user was registered (code)
  - channel: User acquisition channel (code)
  - dx_0: User profile feature
  - dx_1: User profile feature
  - dx_2: User profile feature
  - dx_3: User profile feature
  - gx: User profile feature
  - im: User profile feature

- Purchases table (“sds_purchases.csv”): Transactions/purchases made by registered users.
  - user_id: Unique user identifier
  - purchased_at: Purchase date
  - Value: Purchase value
  - product: Purchased product categorization (code)

### Exploratory data analysis
A more exhaustive explanation of the outcomes of the EDA can be found in the [EDA notebook](./notebooks/eda.ipynb). 
However, here we indicate some of the most relevant observations:
1. Regarding the **purchases** data-frame, 
   1. it was not possible to reach any conclusion regarding the co-dependency
   of purchasing the first product on the second, and vice-versa. 
2. Regarding the **users** data-frame,
   1. Some birth-years went as low as 1700 and beyond 2022 up to more than 2200. These cases
   were removed
   2. The gender is almost never revealed in the data. 
   3. origin_2 and utm_cpg are missing in most occasions.
   4. utm_src and utm_med are missing in the exact same cases.

### Model selection
The conclusions of the model selection can be found in the [model selection notebook](./notebooks/model_selection.ipynb). Here
we provide an overview of the approach and the steps performed. 
#### Hierarchical time series
Regarding the model selection, and given the time constraints, it has been concluded that the best approach
-- as well as one the most commonly used approaches for demand forecasting -- is
[hierarchical time series forecasting](https://otexts.com/fpp3/hierarchical.html).

![](https://www.researchgate.net/profile/Evangelos-Spiliotis/publication/344802492/figure/fig3/AS:949277576683521@1603336819604/Hierarchical-structure-of-the-time-series-included-in-the-examined-dataset.ppm "Logo Title Text 1")
Figure 1. *Example of a hierarchical time series*

Other large companies simply create a large (sometimes recurrent) neural network and, using a massive amount of computation power, make the predictions.
However, these approaches are usually very slow, and as mentioned above, are very computationally expensive, as these models
attempt to find latent connections (e.g, hierarchies) which, in the case above are provided *a priori*.

In our case, the model makes predictions for the bottom layers, and then uses the [variance weighted least squares
(WLS)](https://scikit-hts.readthedocs.io/en/latest/hts.html#hts.functions.optimal_combination) reconciliation method [2] to account for the
interactions within the hierarchies. All of this is implemented using the [sci-kit HTS](https://scikit-hts.readthedocs.io/en/latest/)
package, and is known to be the *state-of-the-art* in demand forecasting, outside neural network approaches.

#### Train and validation dataset construction
In order to choose the train and validation data, a forward validation is performed:

![](https://miro.medium.com/max/1204/1*qvdnPF8ETV9mFdMT0Y_BBA.png)

Figure 2. *Forward cross-validation for time series*

In our case, we perform two folds:
1. The first one uses all the dates up to 180 days before the last date as the train set and the next 90 days as the validation
set. 
2. The second one uses all the dates up to 90 days prior to the last date, and the next 90 days as the validation. 

Once the validation process is complete, the scores are plotted in a box diagram. The metric used in this project has been
the *[mean absolute scaled error (MASE)](https://en.wikipedia.org/wiki/Mean_absolute_scaled_error)* [1]. This consists on dividing
the *mean absolute error (MAE)* of the model by the MAE of the naive model -- that is, the model that
at time *t* uses the last available observation as a prediction -- in our case the last 90 days. 

### Future improvements
#### Use of exogeneous variables
One of the main issues encountered with the hierarchical forecasting methodology is that the munging process for exogeneous
variables is slightly different from the standard, supervised ML data-frame format, and so due to time constraints
it has not been possible to add exogeneous variables -- such as whether the day is a weekend, separating the day into different phases,
adding individual properties of each user, etc. This would have been much easier using a standard ML algorithm, where each entry
corresponds to a time, user_id, the value of the target variable at that time, the lags of that variable, and properties 
dependent on the user. 
#### Other ML models
As explained above, large companies usually generate a data-frame as the one explained in the last sub-section, 
and feed it directly into a large neural network. In the future we would like to compare the results with our model. 

### Business applications
One of the main applications of this forecasting algorithm -- that is, the quarterly monetary value of each user -- can 
be used by the involved company to anticipate the profit for the next quarter. In addition to this, the model can also
be used to allocate more or less assets on each of the locations provided, as well as the possibility of offering
discounts to each user to boost purchases. 


### References
[1]: *Hyndman, R. J.* (2006). "Another look at measures of forecast accuracy", FORESIGHT - Issue 4, June 2006.

[2]: *Hyndman, R. J. & Lee, A. & Earo, W.* (2016) "Fast computation of reconciled forecasts for hierarchical and grouped time series." - Computational Statistics and Data Analysis 97, 16-32.