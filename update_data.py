DAYS_BACK_TO_SCRAPE=1

import pandas as pd
import numpy as np

import selenium as sel
from selenium import webdriver
import requests

from random import randint
import re
import datetime as dt

from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.tag import pos_tag
from nltk.corpus import stopwords
from textblob import TextBlob
import string

import pickle
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor

import os
os.chdir('/Users/matthewkwee/Metis/Metis-7---Engineering')


def main():
	

	crawl_lv_1='https://www.realtor.com/realestateandhomes-search/New-York_NY/show-recently-sold/pg-'
	crawl_lv_2='https://www.realtor.com'

	month_translator={}
	month_translator[1]='Jan'
	month_translator[2]='Feb'
	month_translator[3]='Mar'
	month_translator[4]='Apr'
	month_translator[5]='May'
	month_translator[6]='Jun'
	month_translator[7]='Jul'
	month_translator[8]='Aug'
	month_translator[9]='Sep'
	month_translator[10]='Oct'
	month_translator[11]='Nov'
	month_translator[12]='Dec'

	class RealtorCrawlerPipeline_Lv1:
		def __init__(self, d_ut=7, sleep_time=0, chrome=False):
			self.date_until=None
			self.dl=str(dt.date.today()-dt.timedelta(days=d_ut)).split('-')
			self.date_until=month_translator[int(self.dl[1])]+' '+str(int(self.dl[2]))+', '+self.dl[0]

			self.pages=[]
			self.page_num=1
			self.current_page=None
			self.sleep_time=sleep_time
			self.use_chrome=chrome
			self.tempfindall=None
			self.cookienum=0
			self.lv1_pipeline=True
		
			self.existing_links=None
			with open('RealtorCrawlerLv1_links.txt') as f:
				self.existing_links=[line.strip('\n') for line in f]
			f.close()
			self.existing_links=set(self.existing_links)


		def crawl_next(self):
			print(self.page_num,end='...')
		
			self.cookienum=randint(0,256)
			self.current_page=sel(crawl_lv_1+str(self.page_num), self.sleep_time, self.use_chrome, self.cookienum)

			if botDetected(self.current_page):
				clear_cookie_profile(self.cookienum)
				self.page_num-=1
			self.page_num+=1
			if not self.distill_page():
				print('Stopping...')
				self.output_to_textfile()
				return(self.pages)
			return(True)
	
		def distill_page(self):
			self.tempfindall=re.findall('(/realestateandhomes-detail/.+?)"',self.current_page)
			self.temp_pages=[link for link in self.tempfindall]
			if self.page_num==2:
				self.temp_pages.pop(0)
			self.pages+=self.temp_pages
		
			if self.date_until in self.current_page:
				self.pages=set(self.pages).difference(self.existing_links)
				return(False)
			
			return(True)
	
	
		#def drop_duplicate_pages(self):
		#    self.pages=list(set(self.pages))
	
		def output_to_textfile(self):
			with open('RealtorCrawlerLv1_links.txt','w') as f:
				for link in list(set(self.pages).union(set(self.existing_links))):
					f.write(link)
			f.close()
	
	
	
		def debug(self):
			print(f'Debugging RealtorCrawlerLv1 object:')
			print(f'page_num={self.page_num}')
			print(f'sleep_time={self.sleep_time}')
			print(f'use_chrome={self.use_chrome}')
			print(f'currently_walled={self.currently_walled}')
			print('Variables not shown: current_page')    
	 
	
		def process_current_page(self):
			return self.data.append(create_house_dict(self.current_page))
			
	 
	
	class RealtorCrawlerLv2:
		def __init__(self, scrape_filepath,sleep_time=10, chrome=False):
			self.page_num=0
			self.filepath=scrape_filepath
			self.data=[]
			self.current_page=None
			self.sleep_time=sleep_time
			self.use_chrome=chrome
			self.tempfindall=None
			self.currently_walled=False
		
			with open(self.filepath,'r') as f:
				self.links=[link for link in f]
			f.close()
		
		def crawl_next(self):
			print(self.page_num,end='...')
		
			cookienum=randint(0,256)
			self.current_page=sel(crawl_lv_2+self.links[self.page_num], self.sleep_time, self.use_chrome, cookienum)
		
			if botDetected(self.current_page):
				clear_cookie_profile(cookienum)
				self.page_num-=1
			self.page_num+=1
			return(True)
	
		process_current_page=lambda self:self.data.append(create_house_dict(self.current_page))
		def save_data(self):
			ct=get_time()
			save_name=f'listing_dict_y{ct["years"]}d{ct["days"]}h{ct["hours"]}m{ct["minutes"]}s{ct["seconds"]}'
			with open(save_name,'wb') as f:
				pickle.dump(self.data,f)
			f.close()
	
		def load_data(self,filepath):
			with open(filepath,'rb') as f:
				self.data=pickle.load(f)
			self.page_num=len(self.data)
			f.close()
	
		def debug(self):
			print(f'Debugging RealtorCrawlerLv2 object:')
			print(f'page_num={self.page_num}')
			print(f'filepath={self.filepath}')
			print(f'len(links)={len(self.links)}')
			print(f'sleep_time={self.sleep_time}')
			print(f'use_chrome={self.use_chrome}')
			print(f'currently_walled={self.currently_walled}')
			print('Variables not shown: current_page, links, data')    
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	def soft_cluster(tokens):
		cluster_score={}
		for i in range(cluster_topics):
			cluster_score[f'lda_topic{i}']=0
		for token in listify(tokens):
			if token in xtffn:
				tok_num=xtffn.index(token)
				for topic in range(len(topic_matrix1)):
					cluster_score[f'lda_topic{topic}']+=topic_matrix1[topic][tok_num]
		return(cluster_score)


	def unicodify(to_uni):
		return(''.join(r'\u{:04X}'.format(ord(chr)) for chr in to_uni))

	def listify(to_listify, uni=False):
		if uni:
			listed=re.findall("'(.+?)'",to_listify)
			for i in range(len(listed)):
				listed[i]=unicodify(listed[i])
			return(listed)
		else:
			return(re.findall("'(.+?)'",to_listify))

	def getURL(n):
		return(basic_link+links[n])

	def clear_cookie_profile(cookienum):
		with open(f'cookie_folder/cookies{cookienum}.pkl','wb') as f:
			pickle.dump('',f)
		f.close()
		return(True)

	def sel(url, sleeptime=0, use_chrome=False, cookienum=0):
	
		browser = None
		if use_chrome:
			browser = webdriver.Chrome(chrome_path)
		else:
			browser = webdriver.Safari()
	
		#Make different cookie profiles - realtor.com tracks you partially based on cookies
		try:
			cookies = pickle.load(open(f"cookie_folder/cookies{cookienum}.pkl", "rb"))
			for cookie in cookies:
				browser.add_cookie(cookie)
			print(f'({cookienum})',end='.')
		except:
			pass
	
		browser.get(url)
		scroller=0
		for i in range(sleeptime):
			scroller+=randint(2,4)
			browser.execute_script(f'window.scrollTo(0,{scroller})') 
		code = browser.page_source
		pickle.dump(browser.get_cookies(), open(f"cookie_folder/cookies{cookienum}.pkl","wb"))
	
		browser.close()
		return(code)



	def create_house_dict(html):

		house={}

		house['beds']=re.findall('([0-9.]+)[ ]?bed',html)
		house['baths']=re.findall('([0-9.]+)[ ]?bath',html)
		house['price']=[entry.replace(',','').split('$')[1].strip('"') for entry in re.findall('Last Sold for.{0,10}[0-9,.]+',html)]
		house['description']=re.findall('Property Overview(.+?)</p>',html,re.DOTALL)
		try:
			house['address']=[re.sub('[ \n]+',' ',re.sub('<.+?>','',re.findall('<span itemprop="streetAddress">.{0,500}?postalCode.{0,50}?</span>',html,re.DOTALL)[0],re.DOTALL),re.DOTALL)]
		except:
			house['address']=['N/A']
		house['sqft']=[entry.replace(',','') for entry in re.findall('<li data-label="property-meta-sqft">\n      <span class="data-value">([0-9,.]+)</span> sq ft',html,re.DOTALL)]
		house['sale_date']=re.findall('Sold on ([A-Z][a-z]{0,15}.{0,2}[0-9]{1,2}.{0,2}[0-9]{4})',html)
		house['lot_size']=re.findall('Lot Size Square Feet:.?([0-9]{0,6})',html)
		house['year_built']=re.findall('Year Built:.?([0-9]{0,4})',html)
		house['stories']=re.findall('Stories:.?([0-9]{0,3})',html)
		house['rooms']=re.findall('Total Rooms:.?[0-9]{0,3}',html)
		house['property_type']=re.findall('<div>Type</div>.+?data-original-title=.+?>(.+?)</div>',html,re.DOTALL)
		house['neighborhood']=re.findall('is located in <.+?>([A-Za-z]+)<.+?>',html,re.DOTALL)
		house['borough']=re.findall('neighborhood in the city of <.+?>([A-Za-z]+?, NY)<.+?>',html,re.DOTALL)
	
		#Check public records if no other info available
		if len(house['property_type'])==0:
			house['property_type']=re.findall('Property type: ([A-Za-z]+)',html,re.DOTALL)
		if len(house['year_built'])==0:
			house['year_built']=re.findall('Year built: ([0-9]+)',html,re.DOTALL)


		for key in house:
			if len(house[key])==0:
				house[key]='N/A'
			else:
				house[key]=house[key][0]
		return(house)



	def botDetected(code):
		bot_text='As you were browsing, something about your browser made us think you might be a bot.'
		if bot_text in code:
			return(True)
		return(False)


	def geocode_raw(address, textify=False):
		address+=',New York City, NY'
		link='https://maps.googleapis.com/maps/api/geocode/json?address='
		key='&key=AIzaSyCBJXbbXfVyb8IW44rJ2suo_ltfVo31h3Y'
		address=address.replace(' ', '+')
		address=address.replace('#', '')
		r=requests.get(link+address+key)
		if textify:
			r=r.text
			r.replace('  ','')
		return(r)

	def get_time():
		times={}

		seconds=time()%(60)
		minutes=(time()-seconds)%(3600)/60
		hours=(time()-seconds-minutes*60)%(3600*24)/60/60
		days=(time()-seconds-minutes*60-hours*3600)%(3600*24*365)/60/60/24
		years=(time()-seconds-minutes*60-hours*3600-days*3600*24)/60/60/24/365

		times['seconds']=int(seconds)
		times['minutes']=int(minutes)
		times['hours']=int(hours)
		times['days']=int(days)
		times['years']=int(years)
	
		return(times)


	pipeline_crawler_lv1=RealtorCrawlerPipeline_Lv1(DAYS_BACK_TO_SCRAPE)
		
	while True:
		lv1_pipeline=pipeline_crawler_lv1.crawl_next()
		if lv1_pipeline!=True:
			break
		
	pipeline_to_scrape=pipeline_crawler_lv1.pages

	with open('new_links_to_scrape.txt','w') as f:
		for line in pipeline_to_scrape:
			f.write(line+'\n')
	f.close()

	pipeline_crawler_lv2=RealtorCrawlerLv2('new_links_to_scrape.txt')

	print(f'Links to scrape: {len(pipeline_crawler_lv2.links)}')
	
	resume_from=0
	for i in range(resume_from,len(pipeline_crawler_lv2.links)):
		pipeline_crawler_lv2.crawl_next()
		print(f'{i}',end='...')
		if not pipeline_crawler_lv2.currently_walled:  
			pipeline_crawler_lv2.process_current_page()


	print('Scraping complete.')




	#Clean addon data just like the first time.
	
	print('Constructing addon frame...')
	
	addon_frame=pd.DataFrame(pipeline_crawler_lv2.data)

	na_indicate=lambda s: 0 if s=='N/A' else s

	for column in ['beds','baths','price','address','sqft','year_built','property_type', 'stories','rooms']:
		addon_frame[column]=[na_indicate(item) for item in addon_frame[column]]
		addon_frame=addon_frame[addon_frame[column]!=0]

	addon_frame['building_age']=[int(dt.datetime.now().date().strftime("%Y"))-int(year) for year in addon_frame['year_built']]
	addon_frame.drop(['year_built'],axis=1,inplace=True)
	cut_borough=lambda s: s.split(',')[0].capitalize() if ',' in s else s
	addon_frame['borough']=[cut_borough(n) for n in addon_frame['borough']]
	cut_description=lambda s: s.replace('</span> - ','') if '</span> -' in s else s
	addon_frame['description']=[cut_description(n) for n in addon_frame['description']]
	cut_rooms=lambda s: s.replace('Total Rooms:','') if 'Total Rooms:' in s else s
	addon_frame['rooms']=[cut_rooms(n) for n in addon_frame['rooms']]
	addon_frame=addon_frame[addon_frame['stories']!=0]

	for column in ['beds','baths','price','sqft','stories','rooms', 'stories','building_age']:
		addon_frame[column]=addon_frame[column].astype(float)

	addon_frame.drop(['lot_size'],axis=1,inplace=True)

	#Fill in missing location data for listings
	
	print('Geocoding missing location values...')
	
	indices_to_geocode=[]
	indices_to_geocode+=list(addon_frame.index[addon_frame['neighborhood']=='N/A'])
	indices_to_geocode+=list(addon_frame.index[addon_frame['neighborhood']=='others'])
	indices_to_geocode+=list(addon_frame.index[addon_frame['borough']=='N/A'])
	indices_to_geocode=list(set(indices_to_geocode))
	indices_to_geocode.sort()

	geo_codes={}
	for idx in indices_to_geocode:
		print(idx,end='.')
		geo_codes[idx]=geocode_raw(addon_frame.loc[idx].address)

	for item in geo_codes:
		temp_neighborhood=[comp['long_name'] for comp in geo_codes[item].json()['results'][0]['address_components'] if 'neighborhood' in comp['types']]
		if len(temp_neighborhood)!=0:
			addon_frame.at[item,'neighborhood']=temp_neighborhood[0]
		
	for item in geo_codes:
		temp_borough=[comp['long_name'] for comp in geo_codes[item].json()['results'][0]['address_components'] if 'sublocality' in comp['types']]
		if len(temp_borough)!=0:
			addon_frame.at[item,'borough']=temp_borough[0]

	addon_frame=addon_frame[addon_frame['borough']!='N/A']
	addon_frame=addon_frame[addon_frame['neighborhood']!='N/A']        


	
	#Add polarity and subjectivity to dataframe
	
	print('Calculating sentiment of descriptions...')
	
	pol,sub=[TextBlob(sen).sentiment[0] for sen in addon_frame.description],[TextBlob(sen).sentiment[1] for sen in addon_frame.description]
	addon_frame['pol']=pol
	addon_frame['sub']=sub

	stop_words = stopwords.words('english')

	def remove_noise(tweet_tokens, stop_words = stop_words):
		cleaned_tokens = []

		for token, tag in pos_tag(tweet_tokens):
			token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|''(?:%[0-9a-fA-F][0-9a-fA-F]))+','', token)
			token = re.sub("(@[A-Za-z0-9_]+)","", token)
			token = re.sub("[0-9]+","number_", token)
			token = re.sub("[,.'-:;!]"," ", token)
			token = re.sub("&amp"," ", token)
			token = re.sub("  "," ", re.sub("  "," ", token))
			token=special_cases(token)

			if tag.startswith("NN"):
				pos = 'n'
			elif tag.startswith('VB'):
				pos = 'v'
			elif tag.startswith('JJ') or tag.startswith('NNP'):
				pos = 'del'
			else:
				pos = 'a'

			lemmatizer = WordNetLemmatizer()
			if pos!='del':
				token = lemmatizer.lemmatize(token, pos)
			if len(token) > 0 and token not in string.punctuation and token.lower() not in stop_words and pos!='adj':
				cleaned_tokens.append(token.lower())
		return cleaned_tokens

	# Clean and tokenize descriptions.
	print('Tokenizing descriptions...')
	
	descriptions=addon_frame.description.tolist()
	descriptions_noise=remove_noise(descriptions)
	
	

	with open('word_blacklist.txt','r') as f:
		word_blacklist=[line.strip('\n') for line in f]
	f.close()

	denoised_tokens=[[word for word in dnoise.split(' ') if word not in word_blacklist and word not in ['','\n'] and len(word)>2] for dnoise in descriptions_noise]

	addon_frame['denoised']=denoised_tokens
	addon_frame['denoised']=addon_frame['denoised'].astype(str)



	# Fill in missing borough data
	print('Filling in missing borough data...')
	
	neighborhood_translator={}
	neighborhood_translator['Bronx']='Bronx'
	neighborhood_translator['Brooklyn']='Brooklyn'
	neighborhood_translator['Manhattan']='Manhattan'
	neighborhood_translator['Queens']='Queens'
	neighborhood_translator['Staten Island']='Staten Island'

	neighborhood_translator['Astoria']='Queens'
	neighborhood_translator['Flushing']='Queens'
	neighborhood_translator['Plainview']='Long Island'
	neighborhood_translator['Maspeth']='Queens'
	neighborhood_translator['Roslyn']='Long Island'
	neighborhood_translator['Merrick']='Long Island'
	neighborhood_translator['Glendale']='Queens'
	neighborhood_translator['Bayside']='Queens'
	neighborhood_translator['Melville']='Long Island'
	neighborhood_translator['Manhasset']='Long Island'
	neighborhood_translator['Woodside']='Queens'
	neighborhood_translator['Ridgewood']='Queens'
	neighborhood_translator['Smithtown']='Long Island'
	neighborhood_translator['Kings']='Brooklyn'

	addon_frame['borough']=[neighborhood_translator[untranslated] for untranslated in addon_frame['borough']]
	addon_frame=addon_frame[addon_frame['borough']!='Long Island']



	# Consolidate property type data.
	print('Parsing property types...')
	def property_translator(p_type):
		if 'single' in p_type.lower():
			return 'Single-Family Home'
		elif 'condo' in p_type.lower():
			return 'Condo'
		elif 'multi' in p_type.lower():
			return 'Multi-Family Home'
		elif 'commercial' in p_type.lower():
			return 'Commercial'
		else:
			return 'Other'

	addon_frame['property_type']=[property_translator(ptype) for ptype in addon_frame['property_type']]



	#Cluster descriptions.

	with open('topic_matrix','rb') as f:
		topic_matrix1=pickle.load(f)
	f.close()

	with open('feature_names','rb') as f:
		xtffn=pickle.load(f)
	f.close()




	def soft_cluster(tokens):
		cluster_score={}
		for i in range(64):
			cluster_score[f'lda_topic{i}']=0
		for token in listify(tokens):
			if token in xtffn:
				tok_num=xtffn.index(token)
				for topic in range(len(topic_matrix1)):
					cluster_score[f'lda_topic{topic}']+=topic_matrix1[topic][tok_num]
		return(cluster_score)

	print('Soft clustering descriptions...')

	clusterlist=[soft_cluster(tokenlist) for tokenlist in addon_frame.denoised]
	clusterlist_df=pd.DataFrame(clusterlist)

	for column in clusterlist_df:
		addon_frame[column]=list(clusterlist_df[column])


	print('Creating dummy features...')
	#Create dummy columns for categorical variables
	dummies=pd.get_dummies(addon_frame['property_type'])
	for column in dummies:
		addon_frame[column]=dummies[column]
	
	#dummies=pd.get_dummies(addon_frame['neighborhood'])
	#for column in dummies:
	#    addon_frame[column]=dummies[column]
	
	dummies=pd.get_dummies(addon_frame['borough'])
	for column in dummies:
		addon_frame[column]=dummies[column]
	
	addon_frame.drop(['description','address','sale_date','property_type','borough','neighborhood','denoised'],axis=1,inplace=True)

	print('Updating main dataframe...')

	with open('listing_frame_final','rb') as f:
		listing_frame_v8=pickle.load(f)
	f.close()

	listing_frame_v8=pd.concat([listing_frame_v8,addon_frame], join='outer').fillna(0)
	listing_frame_v8.drop_duplicates(inplace=True)
	
	with open('listing_frame_final','wb') as f:
		pickle.dump(listing_frame_v8,f)
	f.close()
	


	print('Done!')


if __name__ == '__main__':
    main()