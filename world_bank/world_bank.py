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
import numpy as np

st.markdown("**World Bank Data Scraper and Visualizer**")

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
    selected_country_data = country_data[country_data["name"].isin(selected_countries)]
    print(selected_country_data.dtypes)
    st.write("These are the raw data for the country you've selected:")
    st.dataframe(selected_country_data)

          
    map_data = pd.DataFrame({
        'countries' : selected_country_data["name"],
        'lat' : pd.to_numeric(selected_country_data["latitude"]),
        'lon' : pd.to_numeric(selected_country_data["longitude"])
    })

# Adding code so we can have map default to the center of the data
    midpoint = (np.average(map_data['lat']), np.average(map_data['lon']))
    
    st.deck_gl_chart(
                viewport={
                    'latitude': midpoint[0],
                    'longitude':  midpoint[1],
                    'zoom': 4
                },
                layers=[{
                    'type': 'ScatterplotLayer',
                    'data': map_data,
                    'radiusScale': 250,
       'radiusMinPixels': 5,
                    'getFillColor': [248, 24, 148],
                }]
            )

#
#data = pd.DataFrame({
#    'awesome cities' : ['Chicago', 'Minneapolis', 'Louisville', 'Topeka'],
#    'lat' : [41.868171, 44.979840,  38.257972, 39.030575],
#    'lon' : [-87.667458, -93.272474, -85.765187,  -95.702548]
#})
#
## Adding code so we can have map default to the center of the data
#midpoint = (np.average(data['lat']), np.average(data['lon']))
#
#print(data.dtypes)
#
#st.deck_gl_chart(
#            viewport={
#                'latitude': midpoint[0],
#                'longitude':  midpoint[1],
#                'zoom': 4
#            },
#            layers=[{
#                'type': 'ScatterplotLayer',
#                'data': data,
#                'radiusScale': 250,
#   'radiusMinPixels': 5,
#                'getFillColor': [248, 24, 148],
#            }]
#        )
