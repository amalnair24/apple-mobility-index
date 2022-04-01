#!/usr/bin/env python
# coding: utf-8

# # Apple Mobility Trends

# The data is geographically divided into countries/regions, but does have some greater specificity in some larger/capitol cities. The data is broken down into two main categories: walking and driving. This data set measures the change in routing requests since January 13, 2020 across those two categories on a daily abases and per geographical division. A full data description can be found on the Apple web site.  
#   
# This data is sourced daily from the Apple website and is then enriched with other publicly available information.

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

get_ipython().run_line_magic('matplotlib', 'inline')


# In[2]:


apple_mobility = pd.read_csv(r'C:\Users\Jagruti\Downloads\applemobilitytrends-2022-03-29.csv')


# In[3]:


apple_mobility.head()


# In[4]:


apple_mobility.shape


# In[5]:


apple_mobility.info()


# In[6]:


apple_mobility.describe(include='all')


# In[7]:


print(apple_mobility.geo_type.unique())
print(apple_mobility.transportation_type.unique())


# In[8]:


print(apple_mobility.region.nunique())
regions = list(apple_mobility.region.unique())
print(regions)


# In[9]:


apple_total_mob_per_day = apple_mobility.groupby(['region']).sum().reset_index()
apple_total_mob_per_day


# In[10]:


# defining a function for plotting out the cumulative mobility across all transport types for a given region/country in our data

def plot_mobility_total(region_country):
    apple_total_mob_per_day_region = apple_total_mob_per_day[apple_total_mob_per_day.region == region_country]
    apple_total_mob_per_day_region = apple_total_mob_per_day_region.drop(['region'], axis = 1)
    apple_total_mob_per_day_region = apple_total_mob_per_day_region.T
    apple_total_mob_per_day_region.columns = ['Cumulative Mobility across all transport']
    apple_total_mob_per_day_region.plot.line()


# In[11]:


# defining function to take region name as input from the user.

def input_region():
    print('\nWhich region/country mobility report would you like to see?')
    region_name = input()
    if(region_name in regions):
        print('\nBelow plotted is the mobility report for the region/country: ', region_name)
        plot_mobility_total(region_name)
    else:
        print('\nData on this region/country is not available')
        print('\nWanna see the mobility plots of some other region/country ? Enter `Y` or `N`')


# In[12]:


#plotting the input region

input_region()


# The given plot is for the region France where we can observe the mobility of the users till date.

# In[13]:


input_region()


# The above observed plot is for the mobility of the region-Germany where fluctuations are observed till date

# In[14]:


input_region()


# The observations above are for the region-United States till date.

# # Plots for mobility across transport types

# In[15]:


apple_mobility.transportation_type.value_counts()


# From the observations observed we can notice that 3048 conntries/region have data for driving , 1092 country/ region have data for walking & 551 for the transit type.

# In[16]:


#Break into countries/regions and cities
geo_mask = apple_mobility["geo_type"] == "country/region"
mobility_countries = apple_mobility[geo_mask]
mobility_cities = apple_mobility[~geo_mask]
print("There are a total of {} countires and {} cities with provided mobility data.".format(len(mobility_countries),
                                                                                           len(mobility_cities)))


# In[17]:


def get_trans_count(df):
    name = df["geo_type"].iloc[0]
    return df["transportation_type"].value_counts().rename(str(name))
transport_types_count = pd.concat([get_trans_count(mobility_countries), get_trans_count(mobility_cities)], axis=1, sort=False)
transport_types_count


# In[20]:


#Melt into timeseries
id_vars = ["geo_type", "region","transportation_type","sub-region","country"]
mobility_countries_melted = mobility_countries.melt(id_vars=id_vars,var_name="Date",value_name="pct_of_baseline")
mobility_cities_melted = mobility_cities.melt(id_vars=id_vars,var_name="Date",value_name="pct_of_baseline")
mobility_cities_melted.head()


# In[40]:


import plotly.express as px
#Make list of any cities to plot
to_show = ["Atlanta", "Athens", "London"]

#Plot
df = mobility_cities_melted[mobility_cities_melted["region"].isin(to_show)]
fig = px.line(df, x="Date", y="pct_of_baseline", color="transportation_type",
              line_group="region", hover_name="region")
fig.show()


# In[ ]:




