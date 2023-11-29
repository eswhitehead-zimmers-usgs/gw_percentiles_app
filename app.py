# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 09:25:18 2023

@author: eswhitehead-zimmers
"""

import streamlit as st
from app_FUNC import load_dat, plot_dat, tidy_dat


# Format app layout
st.title("Plot Groundwater Percentile Trends in PA")

# Load in data and get user input
trends_all_sites, all_sites = load_dat()

trends_name = tidy_dat(trends_all_sites, all_sites)

option = st.selectbox(
    'Which site do you want to see trends for?',
    trends_name['station_nm'].unique(),
    index=None,
    placeholder="Type or select a site...")

# Create figure from selected data and plot
# But don't try to make plot until there is a choice made
if option is None:
    print("nothing will happen until user choses a site")
else: 
    fig = plot_dat(trends_name, option)
    st.plotly_chart(fig)
    
    
    