# Predicting New York City Housing Prices
 
#### Matthew Kwee, 17 Dec. 2021

## Abstract
In this project, I constructed and compared multiple regression models in order to predict New York City real-estate prices.

I trained both all models from data scraped from realtor.com using Python's Selenium library, then deployed the model on the internet using Flask and Heroku.

## Design
The goal of this project was to create a data pipeline to a web app.

To begin with this project, I scraped three months of data from realtor.com with a web crawler. In order to avoid the site recognizing my crawler as a bot, I created 256 cookie profiles which I loaded into Selenium at random. 

Out of the 9,000 listings I scraped, about 2,400 had all the relevant features. I maximized the number of usable listing by utilizing Google Maps' Geocoding API to fill in missing location data.

I conducted topic modeling on the listings' written descriptions, and created 64 un-named topics. I then soft-clustered each listing based from the resulting topic matrix.

I compared Linear, Ridge, Lasso, Elastic Net, Multilayer Perceptron, and Random Forest models when modeling. Out of all the models, the Random Forest model performed best. I didn't split my data into train-test sets when deploying the final product; while the model did overfit significantly, overfitting will become less of an issue as time passes and my model acquires more and more data.

Next, I wrote a custom "updater"  [script](https://github.com/MK38993/Metis-7---NY-Housing-Market/blob/main/updater_command_.sh) to scrape new listings from realtor.com, pass it through the topic model, use the data to update my model, and push the model to a Git repository containing a Flask web app. The app accepts several features and soft-clusters the written description, if one is provided. I connected this repository to Heroku and deployed the app onto the internet. The Heroku app can be found [here](https://nyc-housing-engineering.herokuapp.com), and automatically updates when the updater script is run. Finally, I configured a cronjob to run the updater script every day.


## Data
The data I scraped from realtor.com is raw HTML code. Using Python's Regular Expressions library, I extracted key features from the code and pulled it into a Pandas dataframe.

Every time the "updater" script is run, all recent listings are scraped from realtor.com and added to the original Pandas dataframe, which is then used to update the Random Forest model (and by extension, the Flask web app).

The features the app accepts are:
- Number of bedrooms/bathrooms, if any
- Square footage
- Number of floors in the building
- Number of rooms in the unit
- Year built
- Building Type (Categorical)
- Borough of New York City (Categorical)
- Written description of building, if provided (Clustered using topic modeling)

## Algorithms
[Discussed in Design section]

## Models
The Random Forest model I constructed consists of 96 decision trees. Its r2 score was 0.83 on all data - when I conducted an 80-20 train-test split, its r2 was 0.88 on training data and 0.65 in test data. I expect that the problem of overfitting will diminish as the dataset grows over time.


## Tools
Selenium for data scraping
Pandas and NumPy for data storage and formatting
Google Maps Geocoding API for filling in missing location data
NLTK for tokenization of listing descriptions
TextBlob for sentiment analysis of descriptions
Gensim for topic modeling descriptions in order to perform soft clustering
Scikit-Learn's Linear, Ridge, Lasso, Elastic Net, Decision Tree, and Random Forest regressors for modeling
TensorFlow's Keras module for constructing a MLP Regressor (It didn't work)
MacOS Command Line scripts for automated data collection and model updates
GitHub API for automatically pushing the Random Forest model to a backup repository
Flask for creating a web app.
Heroku for deploying web app.



## Communication





