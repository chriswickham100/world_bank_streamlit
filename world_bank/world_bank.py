#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 17 15:41:46 2020

@author: chriswickham
"""

import streamlit as st
import requests
import pandas as pd
import json

st.write("This is my World Bank streamlit app")

# For World bank country API documentation, see: 
# https://datahelpdesk.worldbank.org/knowledgebase/articles/898590-country-api-queries

# The World Bank API comes in pages of 50 countries at a time -- the following 
# call finds the number of pages, so we can iterate through each page and 
# collect the information for *all* countries for the streamlit app

page_num = [*range(1,(requests.get("http://api.worldbank.org/v2/country/?format=json")).json()[0]['pages']+1)]

all_country_data = []

for item in page_num:
    api = "http://api.worldbank.org/v2/country/?format=json&page=" + str(item)
    data = requests.get(api).json()[1]
    all_country_data.append(data)
  
# This is flattens the .json to create a single .json of all country data, country_data
    
country_data = []

for page in all_country_data:
    for item in page:
        country_data.append(item)
        
for category in ['region','adminregion','incomeLevel','lendingType']:
    for country in country_data:
        if type(country[category]) != str:
            country[category] = country[category]["value"]            
                        
country_data = pd.read_json(json.dumps(country_data))
    
# Creating a multiselect tool for selecting countries   
    
selected_countries = st.multiselect("Choose your country",country_data["name"])

if selected_countries != []:
    st.write("This is the raw data for the country you've selected:",country_data[country_data["name"].isin(selected_countries)])
          

