## ByRatings assignment
**Author:** Guillem Sala Fernandez
### The challenge
The problem consists of the analysis of an anonymized dataset from an E-commerce transactional database as well as the creation of a predictive model.

The candidate is expected to perform an exploratory analysis of the dataset and to develop a model to predict the quarterly monetary value of each user. More specifically, given a date (present) the model should estimate the aggregated billing of all the purchases each user will make during the following 90 days. Think also about how this model could help to improve business KPIs.

The problem statement is opened on purpose since one of the objectives of this challenge is to evaluate how a problem like this is faced. Regarding the predictive model, the goal is not to build a very complex model to achieve awesome accuracy. This is not a Kaggle competition. We prefer easier models that work well enough and you can explain and justify very well. We are particularly interested in the approach to modelize the problem and evaluate the predictive performance of your solution.

The analysis can be done either in Python or R, although the first is preferred. The results can be presented in any friendly format (Jupyter, R markdown, slides…). Whenever possible, show plots and tables that support your conclusions.

#### Key points:
- Exploratory analysis
- Design of the training and evaluation procedures to build the predictive model
- ETL and feature engineering to build the tables that will be used as input to the predictive model
- Implementation in a production scenario
- Performance evaluation metrics and baselines to be considered
- Business case

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

In our case, the first fold consists on using 50% of the **dates** for the train set and then the **next 90 days** as the validation
set. The next fold uses the 50% of the dates plus the data corresponding to the validation set in the previous fold, and then
uses the next 90 days as the validation set. The algorithm continues as follows until no more validation data
can be used.

Once the validation process is complete, the scores are plotted in a box diagram. The metric used in this project has been
the *[mean absolute scaled error (MASE)](https://en.wikipedia.org/wiki/Mean_absolute_scaled_error)* [1]. This consists on dividing
the *mean absolute error (MAE)* of the model by the MAE of the naive model -- that is, the model that
at time *t* uses the last available observation as a prediction -- in our case the last 90 days. 

## References
[1]: *Hyndman, R. J.* (2006). "Another look at measures of forecast accuracy", FORESIGHT - Issue 4, June 2006.

[2]: *Hyndman, R. J. & Lee, A. & Earo, W.* (2016) "Fast computation of reconciled forecasts for hierarchical and grouped time series." - Computational Statistics and Data Analysis 97, 16-32.