#!/usr/bin/env python
# coding: utf-8

# # Homework 6, Part Two: A dataset about dogs.
# 
# Data from [a FOIL request to New York City](https://www.muckrock.com/foi/new-york-city-17/pet-licensing-data-for-new-york-city-23826/)

# ## Do your importing and your setup

# In[1]:


import pandas as pd
import numpy as np

pd.set_option("display.max_rows", 30000)


# ## Read in the file `NYC_Dog_Licenses_Current_as_of_4-28-2016.xlsx` and look at the first five rows

# In[2]:


df = pd.read_excel ("NYC_Dog_Licenses_Current_as_of_4-28-2016.xlsx", na_values = ['Unknown', 'UNKNOWN', 'unknown'])
df.head(5)


# ## How many rows do you have in the data? What are the column types?
# 
# If there are more than 30,000 rows in your dataset, go back and only read in the first 30,000.

# In[3]:


df.info()


# In[4]:


df.columns


# ## Describe the dataset in words. What is each row? List two column titles along with what each of those columns means.
# 
# For example: “Each row is an animal in the zoo. `is_reptile` is whether the animal is a reptile or not”

# ----
# 
# The dataset contains all dogs licensed in New York, each with a row of its own. The column "spayed or neut" asks if the dogs are either spayed (if female) or neutered (if male). Similarly the column "vaccinated" indicates if they have been vaccinated or not. 
# 
# ----

# # Your thoughts
# 
# Think of four questions you could ask this dataset. **Don't ask them**, just write them down in the cell below. Feel free to use either Markdown or Python comments.

# ----
# 
# 1. How many dogs in NYC are not vaccinated?
# 2. What is the most common breed of dog in the city?
# 3. What zip code has the most dogs?
# 4. What zip code has the highest and lowest percentages of dogs that are not spayed/neutered?
# 
# ----

# # Looking at some dogs

# ## What are the most popular (primary) breeds of dogs? Graph the top 10.

# In[5]:


df['Primary Breed'].value_counts().head(10)

#I ammended my read to make 'unknown' into na values so they won't show here anymore


# ## "Unknown" is a terrible breed! Graph the top 10 breeds that are NOT Unknown

# In[6]:


df['Primary Breed'].value_counts().head(10).sort_values().plot(
kind='barh')


# ## What are the most popular dog names?

# In[7]:


df['Animal Name'].value_counts().head(10)


# ## Do any dogs have your name? How many dogs are named "Max," and how many are named "Maxwell"?

# In[8]:


df['Animal Name'][df['Animal Name'] == 'Paroma'].count()
# What a surprise!


# In[9]:


df['Animal Name'][df['Animal Name'] == 'Max'].count()


# In[10]:


df['Animal Name'][df['Animal Name'] == 'Maxwell'].count()


# ## What percentage of dogs are guard dogs?
# 
# Check out the documentation for [value counts](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.Series.value_counts.html).

# In[11]:


df['Guard or Trained'].value_counts(dropna=False, normalize=True) * 100


# ## What are the actual numbers?

# In[12]:


df['Guard or Trained'][df['Guard or Trained'] == 'Yes'].count()


# In[13]:


df['Guard or Trained'][df['Guard or Trained'] == 'No'].count()


# ## Wait... if you add that up, is it the same as your number of rows? Where are the other dogs???? How can we find them??????
# 
# Use your `.head()` to think about it, then you'll do some magic with `.value_counts()`

# In[14]:


df['Guard or Trained'].value_counts(dropna=False, normalize=True) * 100

#It worked the first time, I guess you mean without the dropna?


# ## Fill in all of those empty "Guard or Trained" columns with "No"
# 
# Then check your result with another `.value_counts()`

# In[15]:


df['Guard or Trained'] = df['Guard or Trained'].fillna("No")


# In[16]:


df['Guard or Trained'].value_counts()


# ## What are the top dog breeds for guard dogs? 

# In[17]:


df['Primary Breed'][df['Guard or Trained'] == 'Yes'].value_counts().head(5)


# ## Create a new column called "year" that is the dog's year of birth
# 
# The `Animal Birth` column is a datetime, so you can get the year out of it with the code `df['Animal Birth'].apply(lambda birth: birth.year)`.

# In[18]:


df['Year'] = df['Animal Birth'].apply(lambda birth: birth.year)
df.head()


# ## Calculate a new column called “age” that shows approximately how old the dog is. How old are dogs on average?

# In[19]:


df['Age'] = 2020 - df['Year']
df.head()


# In[20]:


df['Age'].mean()


# # Joining data together

# In[21]:


df2 = pd.read_csv ("zipcodes-neighborhoods.csv")
df2.head()


# In[22]:


df2.info()


# ## Which neighborhood does each dog live in?
# 
# You also have a (terrible) list of NYC neighborhoods in `zipcodes-neighborhoods.csv`. Join these two datasets together, so we know what neighborhood each dog lives in. **Be sure to not read it in as `df`, or else you'll overwrite your dogs dataframe.**

# In[23]:


#df2[(df2.zip == 11109)]


# In[24]:


merged_full = df.merge(df2, how='left',
        left_on='Owner Zip Code',
        right_on='zip')

#merged_full.zip.isnull().value_counts()
#merged_full[(merged_full.zip.isnull())].sort_values(by='Owner Zip Code')
#merged_full['Owner Zip Code'].isnull().value_counts()

df3 = merged_full.drop(columns=['zip'])
df3
#df3[(df3['neighborhood'].isnull())]


# ## What is the most popular dog name in all parts of the Bronx? How about Brooklyn? The Upper East Side?

# In[25]:


df3['Animal Name'][df3['borough'] == 'Bronx'].value_counts().head(1)


# In[26]:


df3['Animal Name'][df3['borough'] == 'Brooklyn'].value_counts().head(1)


# In[27]:


df3['Animal Name'][df3['neighborhood'] == 'Upper West Side'].value_counts().head(1)


# ## What is the most common dog breed in each of the neighborhoods of NYC?

# In[28]:


#df3.head()


# In[29]:


# df3['Primary Breed'].groupby(df3['neighborhood']).value_counts().groupby(level=0).nlargest(1)


# In[30]:


df3['Primary Breed'].groupby(df3['neighborhood']).value_counts().groupby(level=0).nlargest(1).to_frame()


# In[ ]:





# ## What breed of dogs are the least likely to be spayed? Male or female?

# In[31]:


df3['Spayed or Neut'].groupby(df3['Animal Gender']).value_counts(normalize=True)*100


# ## Make a new column called monochrome that is True for any animal that only has black, white or grey as one of its colors. How many animals are monochrome?

# In[32]:


#df3[df3['Animal Dominant Color'].isnull()]
df3['Animal Dominant Color'] = df3['Animal Dominant Color'].fillna('None')
df3['Animal Secondary Color'] = df3['Animal Secondary Color'].fillna('None')
df3['Animal Third Color'] = df3['Animal Third Color'].fillna('None')


# In[33]:


df3.loc[(df3['Animal Dominant Color'].str.lower().isin(['black','white','gray', 'none'])) | (df3['Animal Secondary Color'].str.lower().isin(['black','white','grey', 'none'])) | (df3['Animal Third Color'].str.lower().isin(['black','white','grey','none'])),'monochrome'] = True


# In[34]:


# df3.loc[(df3['Animal Dominant Color'].str.lower().isin(['black','white','grey', 'none'])),'monochrome'] = True 
# df3.loc[(df3['Animal Secondary Color'].str.lower().isin(['black','white','grey', 'none'])),'monochrome'] = True
# df3.loc[(df3['Animal Third Color'].str.lower().isin(['black','white','grey','none'])),'monochrome'] = True


# In[35]:


df3.loc[(~df3['Animal Dominant Color'].str.lower().isin(['black','white','gray','none'])),'monochrome'] = False
df3.loc[(~df3['Animal Secondary Color'].str.lower().isin(['black','white','gray','none'])),'monochrome'] = False
df3.loc[(~df3['Animal Third Color'].str.lower().isin(['black','white','gray','none'])),'monochrome'] = False


# In[36]:


df3.head(100)


# In[37]:


df3['monochrome'].value_counts()


# ## How many dogs are in each borough? Plot it in a graph.

# In[38]:


df3['Primary Breed'].groupby(df3['borough']).count().plot(kind='barh')


# ## Which borough has the highest number of dogs per-capita?
# 
# You’ll need to merge in `population_boro.csv`

# In[39]:


df4 = pd.read_csv ("boro_population.csv")
df4.head()


# In[40]:


dogsperborough = df3['Primary Breed'].groupby(df3['borough']).count().to_frame().reset_index()
dogsperborough = dogsperborough.rename(columns={'Primary Breed': 'no of dogs'})
dogsperborough


# In[41]:


df5 = dogsperborough.merge(df4, how='left',
        left_on='borough',
        right_on='borough')
df5 = df5.drop(columns=['area_sqmi'])
df5.head()


# In[42]:


df5['dogs per capita'] = df5 ['no of dogs'] / df5 ['population'] * 100
df5.max()


# ## Make a bar graph of the top 5 breeds in each borough.
# 
# How do you groupby and then only take the top X number? You **really** should ask me, because it's kind of crazy.

# In[43]:


#df3.head()


# In[44]:


df3['Primary Breed'].groupby(df3['borough']).value_counts().groupby(level=0).nlargest(5).plot(
kind='barh',
figsize=(10,15))


# ## What percentage of dogs are not guard dogs?

# In[45]:


df3['Guard or Trained'].value_counts(normalize=True)*100


# In[ ]:




