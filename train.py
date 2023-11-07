import sys

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split

from sklearn.feature_extraction import DictVectorizer
from sklearn.model_selection import KFold

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler
import xgboost as xgb
import time
import pickle

# ## Reading data

df = pd.read_csv('inputs/rideshare_kaggle.csv')
df.head(3).T

drop_cols = ['timezone', 'product_id', 'short_summary', 'long_summary', 'windGustTime', 'temperatureHigh',
       'temperatureHighTime', 'temperatureLow', 'temperatureLowTime',
       'apparentTemperatureHigh', 'apparentTemperatureHighTime',
       'apparentTemperatureLow', 'apparentTemperatureLowTime', 'icon',
       'dewPoint', 'pressure', 'windBearing', 'cloudCover', 'uvIndex',
       'visibility.1', 'ozone', 'sunriseTime', 'sunsetTime', 'moonPhase',
       'precipIntensityMax', 'uvIndexTime', 'temperatureMin',
       'temperatureMinTime', 'temperatureMax', 'temperatureMaxTime',
       'apparentTemperatureMin', 'apparentTemperatureMinTime',
       'apparentTemperatureMax', 'apparentTemperatureMaxTime']

df2 = df.drop(drop_cols, axis=1)
df2.columns = df2.columns.str.replace(' ', '_').str.lower()
df2 = df2.set_index('id')

# ## Data split
random_seed = 42

df_full_train, df_test = train_test_split(df2, test_size=0.2, random_state=random_seed)

# ### Missing values
df_full_train = df_full_train.dropna()

y_full_train = df_full_train.price.values
y_test = df_test.price.values

df_full_train = df_full_train.drop(['price'], axis=1)
df_test = df_test.drop(['price'], axis=1)

train_cols = ['distance', 'surge_multiplier',
       'latitude', 'longitude', 'temperature', 'apparenttemperature',
       'precipintensity', 'precipprobability', 'humidity', 'windspeed',
       'windgust', 'visibility', 'source', 'name', 'hour', 'day']

def prepare_df(df_train, df_val, cols):
    
    dv = DictVectorizer(sparse=False)
    
    df_train = df_train[cols]
    df_val = df_val[cols]

    train_dict = df_train.to_dict(orient='records')
    X_train = dv.fit_transform(train_dict)

    val_dict = df_val.to_dict(orient='records')
    X_val = dv.transform(val_dict)
    
    return dv, X_train, X_val

# ## Training on the full train set

dv, X_full_train, X_test = prepare_df(df_full_train, df_test, train_cols)
gbm = xgb.XGBRegressor(colsample_bytree=1.0,
                           learning_rate=0.2,
                           max_depth=7,
                           n_estimators=200, 
                           subsample=1.0,
                           random_state=42)
gbm.fit(X_full_train, y_full_train)
# Get indices of rows with non-null target values
valid_indices = ~np.isnan(y_test)

# Filter out rows with null target values
X_test_notna = X_test[valid_indices]
y_test_notna = y_test[valid_indices]

gbm_pred = gbm.predict(X_test)
gbm_pred_notna = gbm_pred[valid_indices]
rmse_test = mean_squared_error(y_test_notna, gbm_pred_notna, squared=False)
print(f"GBM on the test set gives RMSE: {rmse_test}")

# ## Saving the final model
output_file = 'price_prediction.bin'

with open(output_file,'wb') as f_out: 
    pickle.dump((dv, gbm), f_out)


print(f'The model is saved to {output_file}')