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
    
country_list = []

for page in all_country_data:
    for item in page:
        country_list.append(item)
                
country_names = []

for country in country_list:
    country_names.append(country["name"])
    
print(country_names)

st.multiselect("Choose your country",country_names)

