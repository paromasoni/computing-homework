#!/usr/bin/env python
# coding: utf-8

# # Processing time with `pandas`
# 
# Let's open up some data from [the Census bureau](https://www.census.gov/econ/currentdata/datasets/) - we're going to use **New Home Sales**. The data is formatted... oddly, so I've cleaned it up for you as **home-sales.csv** inside of the **data** folder.
# 
# Open it **without moving it**. Tab autocomplete will help you.

# In[1]:


import pandas as pd
df = pd.read_csv ("home-sales.csv")
df.head()


# In[2]:


df.info()


# ## Creating a datetime column

# In[3]:


df['date'] = pd.to_datetime(df.per_name)
df.head()


# ## Changing the index to the datetime
# 
# Normally the index of the column is just a number.

# In[4]:


df = df.set_index('date')
df.head()


# It's the column on the far left - `0`, `1`, `2`, `3`, `4`... boring and useless! If we use **.set_index** to replace the index with the datetime, though, we can start to have some fun

# In[ ]:





# ## Selecting specific(-ish) dates via the index
# 
# Now that our index is a datetime, we can select date ranges super super easily.
# 
# ### Selecting by month
# 
# Select every row from March, 1999.

# In[5]:


df['1999-03']


# ### Selecting by year
# 
# Select every row from 1996.

# In[6]:


df['1996']


# ## List slices with datetimes
# 
# Just for review, you can use `:` to only select certain parts of a list. This is called **list slicing**.

# In[7]:


# Make our list of fruits
ranked_fruits = ('banana', 'orange', 'apple', 'blueberries', 'strawberries')


# In[8]:


# Start from the beginning, get the first two
ranked_fruits[:2]


# In[9]:


# Start from two, get up until the fourth element
ranked_fruits[2:4]


# In[10]:


# Starting from the third element, get all the rest
ranked_fruits[3:]


# Instead of using boring ol' numbers, we can use **dates instead**.

# ### Getting rows after a certain date
# 
# Select everything *after* March 3rd, 1999.

# In[11]:


df['1999-03-03':]


# ### Getting rows between a certain date
# 
# Select everything *before* July 9th, 1987.

# In[12]:


df[:'1987-07-09']


# # Info on our time series
# 
# If you try to `.plot`, pandas will automatically use the index (the date) as the x axis for you. This makes like **perfect.** because you don't have to think about anything, and calculations automatically have a good axis.
# 
# Graph the number of home sales over time.

# In[13]:


df.val.plot()


# ## Grouping with resample, not with groupby

# Hmmm, looks like something bad might have happened to the housing industry t some point. Maybe we want to see some numbers instead of a graph? To do aggregate statistics on time series in pandas we use a method called `.resample()`, and we're going to tell it **to group the data by year.**
# 
# When we tell it to group by year, we need to give it a **special code**. I always get mine from this StackOverflow post http://stackoverflow.com/a/17001474 because it's much more convenient than the pandas documentation.
# 
# Get the total number of house sales by year.
# 
# *Note: if we didn't have a datetime index, we would use `on='colname'` to specify the column we're resampling on*

# In[14]:


df.resample('A').val.sum()


# Notice that it's **December of every year**. That still looks like too much data, though. What if we zoom out to **every decade** instead?

# In[15]:


df.resample('10Y').val.sum()


# Cool, right?

# ### Graphing
# 
# We can graph these instead of just look at them! Plot all of our years of housing sales, by decade.
# 
# *Note: What is the best kind of graph for this?*

# In[16]:


df.resample('10Y').val.sum().plot(
    kind='barh')


# ## Cyclical data (actually using groupby)
# 
# ### What were the top 5 worst months?
# 
# Start by just simply sorting the dataset to find the top five months that were worst for home sales.

# In[17]:


#df.resample('M').val.head()


# In[18]:


df.val.sort_values(ascending=True).head()


# It seems like there might be a cycle ever year. Maybe houses are sold in the summer and not the winter? To do this we can't use resample - it's for putting time into buckets - we need to **group by the month.**
# 
# ### Getting the month

# We can't ask for the index column as "year" any more, but we can just use `df.index` instead. Look at the date by typing `df.index`.

# In[19]:


df.index.month


# To get the month of each date, it's simply `df.index.month`. If it were a column we would use `df.col_name.dt.month`. Why do we only have to use `.dt` when it's a normal column, and not when it's an index? **I have no idea.**
# 
# Look at the month of each row with `df.index.month`.

# In[20]:


#df.groupby(df.index.month).head()


# ### Doing the groupby to view data by month
# 
# So when we do our groupby, we'll say **hey, we made the groups for you already**. Then we ask for the median number of houses sold. Find the mean number of houses sold each month by using `.groupby(by=df.index.month)`.

# In[21]:


df.groupby(by=df.index.month).mean()


# ### Plot the results

# In[22]:


df.val.groupby(by=df.index.month).mean().plot(
    kind = 'barh')


# In[ ]:





# # More details
# 
# You can also use **max** and **min** and all of your other aggregate friends with `.resample`. For example, what's the **largest number of houses hold in a given year?**

# In[28]:


df.resample('A').val.max().sort_values(ascending=False)
# I don't know if this is correct, because it doesn't say in which month of each year the max number of houses sold were


# How about the fewest?

# In[29]:


df.resample('A').val.min().sort_values()


# In[ ]:




