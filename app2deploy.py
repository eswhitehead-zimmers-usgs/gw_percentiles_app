# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 09:25:18 2023

@author: eswhitehead-zimmers
"""

import streamlit as st
import pandas as pd
import plotly as px
from dataretrieval import nwis


def load_dat():
# This function loads in gw data 
    trends_all_sites = pd.read_csv(r"C:\Users\eswhitehead-zimmers\OneDrive - DOI\Documents\Python_Projects\percentile-trends\scripts\groundwater_percentile\trends_all_sites.csv")
    
    site_nos = trends_all_sites['site_no'].unique()
    
    return trends_all_sites, site_nos

def tidy_dat(trends_all_sites, all_sites):
# This function appends site names to the site number to allow for easier
# site selection
    
    # Convert all_sites to list of strings
    all_sites = list(map(str, all_sites))
    # pull site info for those sites
    siteINFO1 = nwis.get_info(sites = all_sites,
                              siteOutput = 'basic')
    # move site info to dataframe
    pa_active_wells = siteINFO1[0]
    # Pull just station id and station name
    pa_active_wells = pa_active_wells[['site_no','station_nm']]
    
    for name in pa_active_wells['station_nm']:
        words = name.split()
        whole_name =' '.join(words) 
        pa_active_wells['station_nm'][pa_active_wells['station_nm'] == name] = whole_name
     
    pa_active_wells = pa_active_wells.convert_dtypes()
    pa_active_wells['site_no'] = pd.to_numeric(pa_active_wells['site_no'])
    
    # Join station name to trends_all_sites by station id
    trends_names = pd.merge(trends_all_sites, pa_active_wells)
    
    return(trends_names)

def plot_dat(trends_name, station_nm):
# This function plots mann-kendall slope for each percentile of a given site
# Input:
    # trends_all_sites: variable containing all trends for all 76 sites
    # site_no: site number for the site you want trends plotted for. Note:
        # should be given as a string.
# Output:
    # plots trends for specified site_no
      
    # filter out which specific site you want to plot
    trends_name = trends_name[trends_name['station_nm'] == station_nm]
    
    # Create title including site no (which is variable)  
    titl_for_plot = 'Annual water level percentile trends for ' + station_nm
    
    # pretty close to final figure:
    fig = px.line(trends_name, y = 'slope', x = 'level_0', color = 'Trend')
    fig.update_traces(mode='markers')
    #fig.update_yaxes(range=[-6,6])
    fig.add_hline(y=0, line_width=3, line_dash="solid", line_color="green")
    fig.update_layout(
        title_text= titl_for_plot, 
        yaxis=dict(title='slope of trend (%)'),
        xaxis=dict(title='Groundwater Level Percentile'))

    return(fig)



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
    
    
    
