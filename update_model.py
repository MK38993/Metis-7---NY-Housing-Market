

import pandas as pd
import numpy as np

import selenium as sel
from selenium import webdriver
import requests as r

from random import randint
import re
import datetime as dt

from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.tag import pos_tag
from nltk.corpus import stopwords
from textblob import TextBlob
import string

import requests

import pickle
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor

from sklearn.metrics import r2_score

import os
os.chdir('/Users/matthewkwee/Metis/Module 7 - NY Real Estate Regression')











# Run Random Forest Regression
	
with open('listing_frame_final','rb') as f:
	listing_frame_v8=pickle.load(f)
f.close()

print('Constructing Random Forest Regressor...')

X = listing_frame_v8.drop(['price'], axis=1)
regularizer=StandardScaler()
X_reg = regularizer.fit_transform(X)

y = listing_frame_v8['price']


print('Fitting model...')
model = RandomForestRegressor(n_estimators=256,max_features=1.0, random_state=420)
model.fit(X_reg,y)
print('Scoring model...')

# Get the r2 on the validation data
predicted_prices = model.predict(X_reg)
trf = r2_score(y , predicted_prices)
print('Random forest r2 = ', trf)

with open('RandomForestRegressor','wb') as f:
	pickle.dump(model,f)
f.close()


os.chdir('/Users/matthewkwee/Metis/engi_res')

with open('RandomForestRegressor','wb') as f:
	pickle.dump(model,f)
f.close()