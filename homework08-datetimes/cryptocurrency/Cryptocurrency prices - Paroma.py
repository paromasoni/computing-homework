#!/usr/bin/env python
# coding: utf-8

# # Cryptocurrency prices
# 
# * **Filename:**  `cryptocurrencies.csv`
# * **Description:** Cryptocurrency prices for a handful of coins over time.
# * **Source:** https://coinmarketcap.com/all/views/all/ but from a million years ago (I cut and pasted, honestly)
# 
# ### Make a chart of bitcoin's high, on a weekly basis
# 
# You might want to do the cherry blossoms homework first, or at least read the part about `format=` and `pd.to_datetime`.
# 
# *Yes, that's the entire assignment. It isn't an exciting dataset, but it's just dirty enough to make charting this a useful experience.*

# In[1]:


import pandas as pd


# In[2]:


df = pd.read_csv ("cryptocurrencies.csv")


# In[3]:


df.date = pd.to_datetime(df.date)
#df.info()


# In[4]:


df.head()


# In[5]:


df = df.set_index('date')


# In[20]:


df.high = df.high.str.replace(',','').astype(float)


# In[21]:


df.dtypes


# In[28]:


df.head()


# In[36]:


df.resample('W').high.mean().plot()


# In[ ]:





# In[ ]:




