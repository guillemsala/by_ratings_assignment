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
The outcome of the EDA can be found [here](./notebooks/eda.ipynb). 