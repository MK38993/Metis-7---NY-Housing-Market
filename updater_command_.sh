#!/bin/zsh 

say "scraping listing data"

source ~/.zprofile
source ~/.zshrc

conda activate metis

#Set directory.
cd ~
cd Metis
cd Module\ 7\ -\ NY\ Real\ Estate\ Regression

#Scrape new data for the past day.
python update_data.py


#Update the RFR model.
python update_model.py

#Push to GitHub

cd ~
cd Metis
cd engi_res
git remote set-url origin https://MK38993:ghb_PlaceholderForMyAPIKeyItsSecretSorry@github.com/MK38993/engi_res
git pull
git add RandomForestRegressor
git commit -a -m "Updated RFR"
git push origin main

