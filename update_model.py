

import pandas as pd
import numpy as np

import selenium as sel
from selenium import webdriver
import requests as r

from random import randint
import re
import datetime as dt



import requests

import pickle
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor

from sklearn.metrics import r2_score

import os
os.chdir('/Users/matthewkwee/Metis/Metis-7---Engineering')





# Run Random Forest Regression
	
with open('listing_frame_final.bin','rb') as f:
	listing_frame_v8=pickle.load(f)
f.close()

print('Constructing Random Forest Regressor...')

X = listing_frame_v8.drop(['price'], axis=1)

y = listing_frame_v8['price']

print('Fitting model...')
model = RandomForestRegressor(n_estimators=96,max_features=1.0, random_state=420)
model.fit(X,y)
print('Scoring model...')

# Get the r2 on the validation data
predicted_prices = model.predict(X)
trf = r2_score(y , predicted_prices)
print('Random forest r2 = ', trf)

with open('RandomForestRegressor.bin','wb') as f:
	pickle.dump(model,f)
f.close()

os.chdir('/Users/matthewkwee/Metis/engi_res')

with open('RandomForestRegressor.bin','wb') as f:
	pickle.dump(model,f)
f.close()

os.chdir('/Users/matthewkwee/nyc_housing')

with open('RandomForestRegressor.bin','wb') as f:
	pickle.dump(model,f)
f.close()