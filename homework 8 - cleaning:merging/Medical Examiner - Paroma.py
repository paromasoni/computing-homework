#!/usr/bin/env python
# coding: utf-8

# # Medical Examiner Case Archives
# 
# Cook County (Chicago) medical examiner records, taken from [here](https://datacatalog.cookcountyil.gov/Public-Safety/Medical-Examiner-Case-Archive/cjeq-bs86) after discovery via [Data is Plural](https://tinyletter.com/data-is-plural).

# ## Do your importing/setup

# In[1]:


import pandas as pd


# ## Read in the data, check its row count and column types

# In[2]:


df = pd.read_csv("Medical_Examiner_Case_Archive.csv", na_values = 'Data missing')
#df2 = pd.read_csv("case-archive-encoded.csv")


# In[3]:


df.info()


# ## Cleaning up your data
# 
# First you'll want to convert the `Race` and `Gender` columns from codes into actual text to make analysis easier.
# 
# ### Gender codes
# 
# * `-1` - `Data missing`
# * `0` - `Female`
# * `1` - `Male`
# * `2` - `Unknown`
# 
# ### Race codes
# 
# * `-1` - `Data missing`
# * `0` - `American Indian`
# * `1` - `Asian`
# * `2` - `Black`
# * `3` - `Other`
# * `4` - `Unknown`
# * `5` - `White`

# In[4]:


#The CSV file already has the race/gender listed? It's not in codes as far as I can tell


# In[5]:


df.head(20)


# ## What percent of the dataset is men, and what percent is women?
# 
# It should display as **Male** and **Female**, not as numbers.

# In[6]:


df.Gender.value_counts(normalize=True)*100


# ## Getting rid of "Data missing"
# 
# `Unknown` means that officially the gender or race is unknown, while `Data missing` means the record is incomplete. That means "Data missing" should have been `NaN`!
# 
# Go back to your `read_csv` many cells before and make it so that "Data missing" is automatically set as `NaN`.
# 
# - *Tip: Do not use `.replace` for this one!*
# - *Tip: Look at the options for `read_csv`, there's something that lets you specify missing values*
# - *Tip: It isn't `"Data missing"` - think about how you already replaced*
# - *Tip: Be sure you're using an array when you tell it what the 'missing' options are*
# 
# ### After you've done this, re-run all of the the previous cells and confirm that `"Data missing"` does not exist any more

# ## What is the most common race in the dataset? We want percentages.
# 
# We'll come back to this later, I'm just having you check the column for now.

# In[7]:


df.Race.value_counts(normalize=True)*100


# ## Do a `.value_counts()` on the `Opioid Related` column

# In[8]:


df['Opioid Related'].value_counts()


# ## That's weird. Did everyone die from opioids? Try again, but including missing data.

# In[9]:


df['Opioid Related'].value_counts(dropna=False)


# ## Cleaning up True/False columns
# 
# For some reason in this dataset, the True/False columns are either `True` or `NaN`. `NaN` causes a lot of problems, I'd rather have it be false.
# 
# You can use [`fillna`](http://pandas.pydata.org/pandas-docs/version/0.22/generated/pandas.DataFrame.fillna.html) to fill in empty data - it's like `.replace` but for `NaN`.
# 
# ### Replace all `NaN` values with `False` for the "Gun Related" and "Opioid Related" columns.

# In[10]:


df['Opioid Related'] = df['Opioid Related'].fillna('False')
df['Gun Related'] = df['Gun Related'].fillna('False')


# ### Do another value counts on Opioid Related to make sure it has both True and False values

# In[11]:


df['Opioid Related'].value_counts()


# # Back to analysis!

# ## What's the average age people were when they died?

# In[12]:


df.Age.mean()


# ## Let's look at how the oldest people died
# 
# We're just going to browse. Read through how the **oldest 30 people died.**

# In[13]:


df.sort_values(by='Age',ascending=False).head(30)


# ## Seems like a lot of problems with fractures
# 
# ### What's the median age of someone dying from a cause that involves a fracture?
# 
# Are fractures especially dangerous for the elderly?
# 
# - *Tip: Filter for a cause that involves a fracture, then take the median age*
# - *Tip: If you get a "cannot index NA values" error, the problem is it's trying to search `NaN` values and doesn't know what to do with them. You need to tell pandas to count `NaN` as false by setting another option - it isn't `NaN=False`, but it's close!*

# In[14]:


df.Age[df['Primary Cause'].str.contains(r"FRACTURE", na=False)].median()


# ### To get a "compared to what?", what's the median age of _anyone_ dying an accidental death?

# In[15]:


df.Age[df['Manner of Death'].str.contains(r"ACCIDENT", na=False)].median()


# ### What's the median age of each manner of death?
# 
# It looks like different kinds of death might happen to different ages of people. Let's investigate that further.

# In[16]:


df.Age.groupby(df['Manner of Death']).median()
#.sort_values(ascending=False)


# ### Who is the oldest homicide victim?
# 
# It looks like homicide is for young people, so maybe we'll find an interesting outlier?

# In[17]:


df['Manner of Death'] = df['Manner of Death'].fillna('Unknown')
df[(df['Manner of Death'].str.contains(r"HOMICIDE"))].sort_values(by='Age', ascending=False).head(1)


# ## Investigating toxicity-related homicides
# 
# She was old, and was purposefully overdosed on morphine and hydrocodone. Might have been euthenasia? Let's find similar cases.
# 
# ### Find every homicide where the primary cause of death is some sort of toxicity
# 
# Toxicity can just overdose. You should have **ten rows**.
# 
# - *Tip: If you're doing this as one statement, make sure you use your parentheses correctly. If you leave them out, you'll have zero rows*
# - *Tip: You could make a homicides-only dataframe if you wanted to*

# In[18]:


df[(df['Manner of Death'].str.contains(r"HOMICIDE")) & (df['Primary Cause'].str.contains(r"TOXICITY"))]


# ### Okay, nope, we were wrong.
# 
# Those were almost **all from fires**. Apparently homicide is not the best place to go looking for toxicity. What's the most popular manner of death for primary causes involving toxicity?
# 
# - *Tip: Remember that `['colname']` is the same as `.colname`. You can't do `.col with spaces` so you'll need to do `['col with spaces']` a lot in this dataset
# - *Tip: Or I guess if you really wanted to, you could rename your columns to have spaces in them (IF YOU DO THIS DON'T DO IT IN EXCEL BECAUSE IT WILL PROBABLY BREAK YOUR CSV.)*

# In[19]:


#df['Primary Cause'] = df['Primary Cause'].fillna('Unknown')

df['Manner of Death'][df['Primary Cause'].str.contains(r"TOXICITY", na=False)].value_counts()


# ### Okay, toxicity deaths (overdoses) are mostly accidents. Let's look at the first 30 accidental deaths involving toxicity.
# 
# - *Tip: Remember your parentheses!*

# In[20]:


df[(df['Manner of Death'].str.contains(r"ACCIDENT")) & (df['Primary Cause'].str.contains(r"TOXICITY"))].head(30)


# ## Wow, that's a lot of drug overdoses. What's more popular for overdosing: heroin, fentanyl, cocaine, or ethanol?
# 
# You can count something like "COMBINED ETHANOL, NORDIAZEPAM, AND FENTANYL TOXICITY" under both ethanol and fentanyl.
# 
# - *Tip: Search for them individually*

# In[21]:


df['Primary Cause'].str.contains(r"HEROIN").sum()


# In[22]:


df['Primary Cause'].str.contains(r"FENTANYL").sum()


# In[23]:


df['Primary Cause'].str.contains(r"COCAINE").sum()


# In[24]:


df['Primary Cause'].str.contains(r"ETHANOL").sum()


# # Cleaning up Primary Cause
# 
# Let's stop investigating for a second and maybe clean up this "Primary Cause" column.
# 
# ## What are the most common Primary Cause of death? Include `NaN` values
# 
# - *Tip: There is an option that keeps `NaN` values when counting things in a column.*

# In[25]:


#I changed the NaN values to 'Unknown' for a previous question so I'm going to import numpy and chagne it back?
# import numpy as np
# df['Primary Cause'] = df['Primary Cause'].replace('Unknown', np.nan)


# In[26]:


df['Primary Cause'].value_counts(dropna=False).head()


# ## That was horrible looking. I don't want to read through that - how many `NaN` causes of death are there?
# 
# - *Tip: You can use `isnull()` to see if it's missing data, but how do you count the results?*

# In[27]:


df['Primary Cause'].isna().value_counts()


# ## Remove all rows where the primary cause of death has not been filled out.
# 
# - *Tip: confirm that you have 22510 rows when you're done*

# In[28]:


df['Primary Cause'] = df['Primary Cause'].dropna()
df['Primary Cause'].count()


# # Cardiovascular disease
# 
# Cardiovascular disease (heart disease) is the number one or number two killer in America.
# 
# ### Filter for only rows where cardiovascular disease was a primary cause
# 
# - *Tip: I hope you know how to deal with the `NaN` error message by now!*

# In[29]:


df[df['Primary Cause'].str.contains(r"CARDIOVASCULAR DISEASE", na=False)]


# ### What are the different types?

# In[30]:


df['Primary Cause'][df['Primary Cause'].str.contains(r"CARDIOVASCULAR DISEASE", na=False)].value_counts()


# ### Replace all of those with a nice simple 'CARDIOVASCULAR DISEASE'
# 
# - *Tip: you can use `.replace` or `.str.replace`, but they each involve different things! I suggest `.replace`, it looks a little cleaner in this situation*
# - *Tip: for `.replace`, you need to give it more options than usual*
# - *Tip: for `.str.replace`, it won't automatically save back into the column, you need to do that yourself*

# In[31]:


#df['Primary Cause'] = df['Primary Cause'].str.replace((df['Primary Cause'].str.contains(r"CARDIOVASCULAR DISEASE", na=False)), 'CARDIOVASCULAR DISEASE', values='str')
# TypeError: 'Series' objects are mutable, thus they cannot be hashed 
#FROM STACK OVERFLOW --- df.sport.str.replace(r'(^.*ball.*$)', 'ball sport')

df['Primary Cause'] = df['Primary Cause'].str.replace(r".*CARDIOVASCULAR DISEASE.*", "CARDIOVASCULAR DISEASE")


# ### Check the top 5 primary causes. Cardiovascular disease should be first with about 28.4%

# In[32]:


df['Primary Cause'].value_counts(normalize=True).head()*100


# We could also clean up gunshots, but... let's just move on.

# # The Opioid Epidemic
# 
# America has a [big problem with fentanyl](https://www.theatlantic.com/health/archive/2018/05/americas-opioid-crisis-is-now-a-fentanyl-crisis/559445/) and other opioids.
# 
# ## Find all of the rows where fentanyl was part of the primary cause of death
# 
# We don't need `na=False` any more because we *dropped the rows without primary causes*.

# In[33]:


df['Primary Cause'].isna().value_counts()
#.dropna() doesn't seem to be working even though i did save it back into the variable.


# In[34]:


df[df['Primary Cause'].str.contains(r"FENTANYL", na=False)]


# ## Fentanyl and race
# 
# In the late 80's and 90's, the [crack cocaine epidemic](https://en.wikipedia.org/wiki/Crack_epidemic) swept through inner cities in the US. It was treated primarily as a crime problem, while many people say fentanyl and heroin overdoses are being treated as a medical problem due to the racial differences - the crack epidemic mainly affected Black communities, while fentanyl seems to be a problem for everyone.
# 
# ### How does the racial breakdown of fentanyl deaths compare to the racial breakdown of other causes of death? How about compared to causes of accidental death?

# In[35]:


df.Race[df['Primary Cause'].str.contains(r"FENTANYL", na=False)].value_counts()


# In[36]:


#df['Primary Cause'].groupby(df.Race).value_counts().groupby(level=0).nlargest(5).reset_index(level=0, drop=True).to_frame() 
#This is for all causes of death


# In[37]:


df.Race[df['Manner of Death'].str.contains(r"ACCIDENT", na=False)].value_counts()


# ### Now compare it to homicides

# In[38]:


df.Race[df['Manner of Death'].str.contains(r"HOMICIDE", na=False)].value_counts()


# ### Now compare it to suicide

# In[39]:


df.Race[df['Manner of Death'].str.contains(r"SUICIDE", na=False)].value_counts()


# ## These differences seems kind of crazy
# 
# Let's look at all of these at once: I want a breakdown of the most common manners of death for **men**, based on race.
# 
# Percentages, please, not raw numbers.
# 
# You can look at women, too, although I think the numbers are more surprising for men.

# In[40]:


df['Manner of Death'][(df.Gender == 'Male')].groupby(df.Race).value_counts(normalize=True)*100


# In[41]:


df['Manner of Death'][(df.Gender == 'Female')].groupby(df.Race).value_counts(normalize=True)*100


# ## Back to drugs: what is the most popular opioid-related primary cause of death that does NOT involve fentanyl?
# 
# - *Tip: Pay attention to your column names! There's one that might tell you if something is opioid-related...*
# - *Tip: Usually you can use `not` or `!` to means "not", but for pandas and `.isin` or `.str.contains` you need to use `~`*
# - *Tip: For "and" in pandas you'll need to use `&`, and make sure all of your clauses have parens around them, e.g. `df[(df.col1 = 'A') & (df.col2 = 'B')]`.*

# In[42]:


#df.head()


# In[43]:


df['Primary Cause'][(df['Opioid Related'] == True) & (~df['Primary Cause'].str.contains(r"FENTANYL", na=False))].value_counts().head()


# # How do heroin and fentanyl deaths compare?
# 
# ## Count the number of deaths involving heroin, the number of deaths involving fentanyl, and the number of deaths involving both.
# 
# - *Tip: This will take 3 different statements*
# - *Tip: You should get `813` that include both*

# In[44]:


df['Case Number'][df['Primary Cause'].str.contains(r"FENTANYL", na=False)].count()


# In[45]:


df['Case Number'][df['Primary Cause'].str.contains(r"HEROIN", na=False)].count()


# In[46]:


df['Case Number'][(df['Primary Cause'].str.contains(r"FENTANYL", na=False)) & (df['Primary Cause'].str.contains(r"HEROIN", na=False))].count()


# ## That's weird.
# 
# I heard fentanyl really surpassed heroin in the past few years. Let's see how this 
# 
# ### Pull the year out and store it in a new column called `year`
# 
# If you run `df['Date of Incident'].str.extract("(\d\d\d\d)", expand=False)`, it will pull out the year of each incident. **Store this in a new column called `year`.**
# 
# (It's regular expression stuff. `\d\d\d\d` means "four numbers in a row", and `()` + `.str.extract` means "pull it out".)

# In[47]:


df['year'] = df['Date of Incident'].str.extract("(\d\d\d\d)", expand=False)


# ### What is the datatype of the new `year` column?

# In[48]:


df.year.dtype
#object


# ## Convert this new column to an integer and save it back on top of itself
# 
# - *Tip: This uses is your friend `.astype`*
# - *Tip: Make sure to save it back on top of itself!*

# In[49]:


df.year = df.year.astype(int)


# ## Confirm the column is a number

# In[50]:


df.year.dtype


# ## Plot the number of opioid deaths by year
# 
# If you'd like to make it look nicer, do some sorting and get rid of 2018.
# 
# - *Tip: Think of it in a few steps. First, filter for opioid deaths. Then get the number of deaths for each year. Then plot it.*
# - *Tip: What's up with 2018? Why's it look so weird? Can you get rid of it? Remember to use lots of parens!*
# - *Tip: Make sure the earliest year is on the left. You might need to sort by something other than values.*

# In[51]:


#df[df.year == 2018]


# In[52]:


df['Opioid Related'][df['Opioid Related']==True].groupby(df.year).value_counts().plot(kind='barh')

# 2018 doesn't look weird except that it's lower than most, is that wrong??


# In[ ]:





# ## Plot the number of fentanyl deaths by year, and the number of heroin deaths by year
# 
# - *Tip: You'll want to look up how to use `ylim` - it will let you set each graphic to use the same scale. This should be separate graphics.*
# - *Tip: Pay attention to the numbers on your axes. `sort_index()` will be your friend.*
# - *Tip: You should probably get rid of 2018*

# In[53]:


df['Primary Cause'][df['Primary Cause'].str.contains(r"FENTANYL", na=False)].groupby(df.year).count().plot(kind='barh')


# In[54]:


#df['Primary Cause'].str.contains(r"FENTANYL", na=False).groupby(df.year).count()


# In[55]:


df['Primary Cause'][df['Primary Cause'].str.contains(r"HEROIN", na=False)].groupby(df.year).count().plot(kind='barh')


# In[ ]:





# ## How does this compare to gun deaths?

# In[56]:


df['Primary Cause'][df['Primary Cause'].str.contains(r"GUN", na=False)].groupby(df.year).count().plot(kind='barh')


# ## But hey: numbers can lie pretty easily!
# 
# The numbers are just so low in 2014 and much higher in 2017. What's going on there?
# 
# Well, maybe **there just isn't as much data from the earlier years**. Plot how many entries there are for each year.

# In[57]:


df['Primary Cause'][(df['Primary Cause'].str.contains(r"GUN", na=False))].groupby(df.year).count()


# And we don't know the best way to fix that up yet, so instead I'm going to give you a present.
# 
# # Is the true lesson here, don't move to Cook County, Illinois?
# 
# Cook County is basically Chicago. It's probably just certain areas that are trouble, right? Let's investigate that without even having a clue how mapping works.
# 
# ## Fun bonus: Making cheating maps
# 
# ### Make a new dataframe of every death in the actual city of Chicago

# In[58]:


dfchic = df[df['Incident City'] == 'CHICAGO']
dfchic.head()


# ### Confirm this new dataframe has 13,627 rows

# In[59]:


dfchic.shape

#I can't figure out why there are 77 additional rows. They are not null values.


# ### Use lat and long in the worst way possible to make a map
# 
# Use `longitude` and `latitude` and `plot` to make a rough map of the city. Chicago [looks like this](https://en.wikipedia.org/wiki/File:DuPage_County_Illinois_Incorporated_and_Unincorporated_areas_Chicago_Highlighted.svg)
# 
# - *Tip: Use the `latitude` and `longitude` columns*
# - *Tip: You don't want a line graph, of course. Or a bar. What kind is the kind with dots on it?*
# - *Tip: Use something like like `figsize=(10,5)` to specify the height and width of the map (but, you know, with better numbers that make it look like chicago)*

# In[60]:


dfchic.plot(kind='scatter',
           x='longitude',
           y='latitude',
           figsize= [7,14])


# ## Now let's find out where to live
# 
# Make a map of every non-homicide death in Chicago, then plot the homicides on top of it.
# 
# Use the `ax=df.plot` trick from the beer cans assignment to plot all of the rows representing homicides vs non-homicides. You can use `color='red'` to make one of them red, and `alpha=0.05` to make each mark very transparent to allow them to layer on top of each other.

# In[61]:


ax = dfchic[~(df['Manner of Death'] == 'HOMICIDE')].plot(kind='scatter',
           x='longitude',
           y='latitude',
           figsize= [7,14],
            alpha=0.5)
dfchic[df['Manner of Death'] == 'HOMICIDE'].plot(
            kind='scatter',
            ax=ax,
           x='longitude',
           y='latitude',
           figsize= [7,14],
            color='red')


# ## Never tell anyone I let you do that.
# 
# But you want to see something actually completely legitimately insane?
# 
# **Chicago is one of the most segregated cities in America.** If you'd like to see this for yourself, make a map of `Race`. Plot black vs white in a way similar to what we did above.

# In[62]:


ax = df[df.Race == 'White'].plot(kind='scatter',
           x='longitude',
           y='latitude',
           figsize= [7,14],
            alpha=0.5)
dfchic[df.Race == 'Black'].plot(
            kind='scatter',
            ax=ax,
           x='longitude',
           y='latitude',
           figsize= [7,14],
            color='red')


# Yup.

# In[ ]:




