#!/bin/zsh 

say "scraping listing data"

source ~/.zprofile
source ~/.zshrc

conda activate metis

#Set directory.
cd ~
cd Metis
cd Metis-7---Engineering

#Scrape new data for the past day.
python update_data.py


#Update the RFR model.
python update_model.py
#Push to backup repository
cd ~
cd Metis
cd engi_res
git remote set-url origin https://MK38993:ghb_PlaceholderForMyAPIKeyItsSecretSorry@github.com/MK38993/engi_res
git pull
git add RandomForestRegressor.bin
git commit -a -m "Updated RFR"
git push origin main


#Update Heroku app
cd ~
cd nyc_housing
git add .
git commit -am "Updating resources"
git push heroku master
