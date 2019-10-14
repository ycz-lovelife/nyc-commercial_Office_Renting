import numpy as np
import pandas as pd
import pickle 

#load file from pickle
with open('pickle-files/dataframe_1008.pkl', 'rb') as picklefile: 
    dataframe = pickle.load(picklefile)

#transform to dataframe
df = pd.DataFrame(dataframe)

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.linear_model import LinearRegression, Lasso, LassoCV, Ridge, RidgeCV
from sklearn.metrics import r2_score


#specify columns to use for modeling

X = df.drop(['title','address','floor_level',                 'post_date','construction_type',                'public_transit','rate_term','rate_price'],axis=1)

y = df['rate_price']


# ## Observe Dependent Variable (Y) distribution
test = df[['sqft', 'nearby_public_transit', 'days_of_listing','rate_price']]

import seaborn as sns
import matplotlib.pyplot as plt
sns.set()

sns.pairplot(test)
plt.show()


# ## Standard Regression

def split_and_validate_scaled(X, y):
    '''
    For a set of features and target X, y, perform a 80/20 train/val split, 
    fit and validate a linear regression model, and report results
    '''
    
    # perform train/val split
    X_train_val, X_test, y_train_val, y_test =         train_test_split(X, y, test_size=0.2, random_state=12345)
    
    X_train, X_val, y_train, y_val =         train_test_split(X_train_val, y_train_val, test_size = 0.2, random_state = 10)
    
    numeric = ['sqft','nearby_public_transit','days_of_listing','sqft_reverse', 'transit_reverse', 'daysListing_poly']
    #'sqft_reverse', 'transit_reverse', 'daysListing_poly'

    X_train_1 = X_train[numeric]
    X_train_2 = X_train.drop(columns = numeric)
    
    X_val_1 = X_val[numeric]
    X_val_2 = X_val.drop(columns = numeric)
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train_1.values)
    X_val_scaled = scaler.transform(X_val_1.values)
    
    
    # fit linear regression to training data
    lr_model = LinearRegression()
    lr_model.fit(X_train_1.join(X_train_2), y_train)
    
    # score fit model on validation data
    train_score = lr_model.score(X_train_1.join(X_train_2), y_train)
    val_score = lr_model.score(X_val_1.join(X_val_2), y_val)
    
    # report results
    print('\nTraining R^2 score was:', train_score)
    print('\nValidation R^2 score was:', val_score)
    
    print('Feature coefficient results: \n')
    for feature, coef in zip(X.columns, lr_model.coef_):
        print(feature, ':', f'{coef:.2f}') 
#     return X_val_1.join(X_val_2), y_val, lr_model


split_and_validate_scaled(X, y)


# **Basic linear regression model doesn't work in this case!**

# ## Reverse Regression


X_reverse = X.copy()

X_reverse['sqft_reverse'] = 1/X_reverse['sqft']
X_reverse['transit_reverse'] = 1/X_reverse['nearby_public_transit']


split_and_validate_scaled(X_reverse, y)


# Validation R^2 improved to 0.53 after adding two 1/X variables!

# ## Polynomial Regression

# In[13]:


X_poly = X_reverse.copy()

X_poly['daysListing_poly'] =  X_reverse['days_of_listing'] ** 2


split_and_validate_scaled(X_poly, y)


# Validation R^2 increased by 0.004 by increasing a polynomial variable

# ## Interaction Features


X_interactive = X_poly.copy()

X_interactive['sqft_x_listingDays'] =  X_poly['sqft'] * X_poly['days_of_listing']
X_interactive['sqft_x_transit'] = X_poly['sqft'] * X_poly['nearby_public_transit']


split_and_validate_scaled(X_interactive, y)


# ## Cross Validation


from sklearn.model_selection import cross_val_score
lm = LinearRegression()

cross_val_score(lm, X_poly_train, y_poly_train, cv=10, scoring='r2')



from sklearn.model_selection import KFold
kf = KFold(n_splits=10, shuffle=True, random_state = 1000)

print(np.mean(cross_val_score(lm, X_poly_train, y_poly_train, cv=kf, scoring='r2')))
# print(np.mean(cross_val_score(lm_reg, X, y, cv=kf, scoring='r2')))


# ## LassoCV

from sklearn.linear_model import LinearRegression, Lasso, LassoCV, Ridge, RidgeCV
from sklearn.metrics import r2_score

#LASSO CV
def lasso_scaled(X, y):
    '''
    For a set of features and target X, y, perform a 80/20 train/val split, 
    fit and validate a linear regression model, and report results
    '''
    
    # perform train/val split
    X_train_val, X_test, y_train_val, y_test =         train_test_split(X, y, test_size=0.2, random_state=10)
    
    X_train, X_val, y_train, y_val =         train_test_split(X_train_val, y_train_val, test_size = 0.2, random_state = 10)
    
    numeric = ['sqft','nearby_public_transit','days_of_listing', 'sqft_reverse','transit_reverse','daysListing_poly']

    X_train_1 = X_train[numeric]
    X_train_2 = X_train.drop(columns = numeric)
    
    X_val_1 = X_val[numeric]
    X_val_2 = X_val.drop(columns = numeric)
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train_1.values)
    X_val_scaled = scaler.transform(X_val_1.values)
    
    
    
    
    alphavec = 10**np.linspace(1,2,300)

    ridge_model = RidgeCV(alphas = alphavec, cv=10)
    ridge_model.fit(X_train_1.join(X_train_2), y_train)
    
    
    
    
#      # score fit model on validation data
    train_score = ridge_model.score(X_train_1.join(X_train_2), y_train)
    val_score = ridge_model.score(X_val_1.join(X_val_2), y_val)
    
#     report results
    print('\nTraining R^2 score was:', train_score)
    print('\nValidation R^2 score was:', val_score)
    
    print('Feature coefficient results: \n')
    for feature, coef in zip(X.columns, ridge_model.coef_):
        print(feature, ':', f'{coef:.2f}') 
    
#     print (lasso_model.alpha_)



np.set_printoptions(precision=10)



lasso_scaled(X_poly, y)


# Opps, regularization makes validation score worse, which means data is still underrepresented by the model. Need more data to feed in.

# ## Test on Testing Data

X_rest, X_test, y_rest, y_test =     train_test_split(X_interactive, y, test_size=0.2, random_state=10)

numeric = ['sqft','nearby_public_transit','days_of_listing','sqft_reverse', 'transit_reverse', 'daysListing_poly']

X_rest_1 = X_rest[numeric]
X_rest_2 = X_rest.drop(columns = numeric)

X_test_1 = X_test[numeric]
X_test_2 = X_test.drop(columns = numeric)

scaler = StandardScaler()
X_rest_scaled = scaler.fit_transform(X_rest_1.values)
X_test_scaled = scaler.transform(X_test_1.values)    
    

# fit linear regression to training data
lr_model = LinearRegression()
lr_model.fit(X_rest_1.join(X_rest_2), y_rest)

# score fit model on validation data
# train_score = lr_model.score(X_train_1.join(X_train_2), y_train)
test_score = lr_model.score(X_test_1.join(X_test_2), y_test)

# report results
# print('\nTraining R^2 score was:', train_score)
print('\nTesting R^2 score is:', test_score)

