# This is a reference script for all of the World Bank API's 

# Maybe build an API builder by working through this: 
# https://datahelpdesk.worldbank.org/knowledgebase/topics/125589-developer-information


# Country API's: 

import requests
import pandas as pd
import json
import streamlit as st

def countries_api():
    page_num = [*range(1,(requests.get("http://api.worldbank.org/v2/country/?format=json")).json()[0]['pages']+1)]
    all_country_data = []

    for item in page_num:
        api = "http://api.worldbank.org/v2/country/?format=json&page=" + str(item)
        data = requests.get(api).json()[1]
        all_country_data.append(data)
  
# This flattens the .json to create a single .json of all country data, country_data
    
    country_data = []
    
    for page in all_country_data:
        for item in page:
            country_data.append(item)
            
    for category in ['region','adminregion','incomeLevel','lendingType']:
        for country in country_data:
            if type(country[category]) != str:
                country[category] = country[category]["value"]            
                            
    country_data = pd.read_json(json.dumps(country_data))
    
    return(country_data)

st.markdown("**World Bank API Builder**")

data_format = st.multiselect("What format do you want your data in?",['XML','JSON','JSONP','JSON-stat'])

indicator_families = ["Poverty and Inequality","People","Environment","Economy","States and Markets","Global Links"]

if st.checkbox("Are you interested in development indicators?"): 
    indicators_family = st.multiselect("What family of indicators are you interested in?",indicator_families)
    
if st.checkbox("Are you interested in data related to International Debt Statistics?",key=1):
    st.write("indicators")
    
if st.checkbox("Are you interested in data related to Doing Business?",key=2):
    st.write("x")
    
if st.checkbox("Are you interested in data related to Human Capital?",key=3):
    st.write("y")
    
if st.checkbox("Are you interested in data related to Subnational Poverty?",key=4):
    st.write("z_")
    
if st.checkbox("Are you interested in data related to International Debt Statistics?",key=5):
    st.write("p")

