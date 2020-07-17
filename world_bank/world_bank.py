#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 17 15:41:46 2020

@author: chriswickham
"""

import streamlit as st
import requests
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
             
# Creating a list of country names, country_names  
        
country_names = []

for country in country_data:
    country_names.append(country["name"])
    
# Creating a multiselect tool for selecting countries   
    
selected_country_data = []
    
selected_countries = st.multiselect("Choose your country",country_names)

# Showing the results of the multiselect tool:

#THIS IS BUGGY - SOMETHING's HAPPENING HERE decided to walk away and come back

for country in country_data:
    print("COUNTRY",country)
    for selected_country in selected_countries:
        print("SELECTED_COUNTRY",selected_country)
        if country['name'] == selected_country:
            print("THIS IS SELECTED COUNTRY NAME",country['name'])
            print("THIS IS SELECTED COUNTRY DATA",country)
            selected_country_data = selected_country_data.append(country)
            
if selected_countries != []:
    st.write("This is the json containing data for the countries you've chosen:", selected_countries)
            
st.write(selected_country_data)
            

