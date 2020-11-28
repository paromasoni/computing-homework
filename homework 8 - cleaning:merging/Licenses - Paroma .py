#!/usr/bin/env python
# coding: utf-8

# # Texas Licenses
# 
# I originally got this dataset from the [License Files page](https://www.license.state.tx.us/licensesearch/licfile.asp) from the Texas Department of Licensing and Regulation, but they've changed around since then! I'm pretty sure it's [this dataset](https://www.opendatanetwork.com/dataset/data.texas.gov/7358-krk7), but we'll just use a local version instead of the most current.

# # PART ONE: OPENING UP OUR DATASET

# ## 0. Do your setup
# 
# Import what you need to import, etc.

# In[1]:


import pandas as pd


# ## 1. Open the file
# 
# We'll start with `licfile.csv`, which is a list of licenses.

# In[2]:


df = pd.read_csv ("licfile.csv")
df.head()


# ## 2. That looks terrible, let's add column names.
# 
# It apparently doesn't have headers! **Read the file in again, but setting your own column names**. Their [current data dictionary might not perfectly match](https://www.opendatanetwork.com/dataset/data.texas.gov/7358-krk7), but you can use it to understand what the columns are. For the dataset we're using, the order goes like this:
# 
# * LICTYPE
# * LICNUMBER
# * BIZCOUNTY
# * BIZNAME
# * BIZLINE1
# * BIZLINE2
# * BIZCITYSTATE
# * BIZTELEPHONE
# * EXPIRATION
# * OWNER
# * MAILLINE1
# * MAILLINE2
# * MAILCITYSTATE
# * MAILCOUNTYCODE
# * MAILCOUNTY
# * MAILZIP
# * TELEPHONE
# * LICSUBTYPE
# * CEFLAG
# 
# **Note:** You can rename the columns to things that make sense - "expiration" is a little more manageable than "LICENSE EXPIRATION DATE (MMDDCCYY)". I've named my License Type column LICTYPE, so if you haven't you'll have to change the rest of my sample code to match.

# In[3]:


# df = pd.read_csv ("licfile.csv", names=['LICTYPE','LICNUMBER','BIZCOUNTY','BIZNAME','BIZLINE1','BIZLINE2','BIZCITYSTATE','BIZTELEPHONE','EXPIRATION','OWNER','MAILLINE1','MAILLINE2','MAILCITYSTATE','MAILCOUNTYCODE','MAILCOUNTY','MAILZIP','TELEPHONE','LICSUBTYPE','CEFLAG'])
# df.head()


# In[4]:


#df.info()


# # 3. Force string columns to be strings
# 
# The county code and expiration dates are being read in as numbers, which is going to cause some trouble later on. You can force a column to be a certain type (most usually strings) when reading it in with the following code:
# 
#     df = pd.read_csv("your-filename.csv", dtype={"colname1": str, "colname2": str})
# 
# You don't need to do it for every column, just the ones you want to force!
# 
# **Re-import the file, forcing the expiration date, license number, mailing address county code, mailing zip code and telephone to all be strings.**

# In[5]:


df = pd.read_csv ("licfile.csv", names=['LICTYPE','LICNUMBER','BIZCOUNTY','BIZNAME','BIZLINE1','BIZLINE2','BIZCITYSTATE','BIZTELEPHONE','EXPIRATION','OWNER','MAILLINE1','MAILLINE2','MAILCITYSTATE','MAILCOUNTYCODE','MAILCOUNTY','MAILZIP','TELEPHONE','LICSUBTYPE','CEFLAG'],
                  dtype={ 'LICNUMBER': str,'BIZTELEPHONE': str, 'EXPIRATION': str,'MAILCOUNTYCODE': str,'TELEPHONE': str})
df.head()


# Check the data types of your columns to be sure! If you do it right they'll be `object` (not `str`, oddly).

# In[6]:


df.info()


# In[7]:


df.dtypes


# In[8]:


df.head()


# ## 4. Convert those expiration dates from MMDDYYYY to YYYY-MM-DD
# 
# You can use list slicing with `.str` (we did `dt.per_name.str[:4]` for the home data stuff once), `pd.to_datetime`, or a hundred other methods.

# In[9]:


df['EXPIRATION']= pd.to_datetime(df['EXPIRATION'], format='%m%d%Y')


# Check the first five expirations to make sure they look right.

# In[10]:


#df.dtypes
df.head()


# # PART TWO: LOOKING AT LICENSES

# ## 5. What are the top 10 most common licenses?

# In[11]:


df['LICTYPE'].value_counts().head(10)


# ## 6. What are the top 10 least common?

# In[12]:


df['LICTYPE'].value_counts().sort_values().head(10)


# ## 7. Try to select everyone who is any type of electrician.
# 
# You're going to get an error about `"cannot index with vector containing NA / NaN values"`. Let's work our way in there.

# In[13]:


# Yes I know I left this in here, it's a learning experience!
#df[df['LICTYPE'].str.contains("Electrician")]


# In[ ]:





# ## 8. How many of the rows of LICTYPE are NaN?

# In[14]:


df['LICTYPE'].isna().value_counts()


# Over 7000 licenses don't have types! As a result, when we look for license types with electricians - aka do `df['LICTYPE'].str.contains("Electrician")` - we get three results:
# 
# * `True` means `LICTYPE` exists and contains `"Electrician"`
# * `False` means `LICTYPE` exists and does not contain `"Electrician"`
# * `NaN` means `LICTYPE` does not exist for that row

# ## 9. Actually getting everyone who is an electrician

# This doesn't work when trying to select electricians, though, as NaN is a no-go for a filter. We *could* filter out everywhere the LICTYPE is null, but we could also cheat a little and say "replace all of the `NaN` values with `False` values."
# 
# `.fillna(False)` will take every `NaN` and replace it with `False`. 

# In[15]:


df['LICTYPE'] = df['LICTYPE'].fillna(False)


# In[16]:


df['LICTYPE'].isna().value_counts()


# In[17]:


df['LICTYPE'] = df['LICTYPE'].astype(str)


# ## 10. What's the most popular kind of electrician?

# In[18]:


df['LICTYPE'][df['LICTYPE'].str.contains("Electrician")].value_counts()


# ## 11. Graph it, with the largest bar on top.

# In[19]:


df['LICTYPE'][df['LICTYPE'].str.contains("Electrician")].value_counts().sort_values().plot(
    kind='barh')


# ## 12. How many sign electricians are there?
# 
# There are a few ways to do this one.

# In[20]:


df['LICTYPE'][(df['LICTYPE'].str.contains("Electrician")) & (df['LICTYPE'].str.contains("Sign"))].value_counts()


# # PART THREE: LOOKING AT LAST NAMES

# ## 13. Extract every owner's last name
# 
# You want everything before the comma. We've done this before (in a few different ways!).
# 
# * **Hint:** If you get an error about missing or `NaN` data, you might use `.fillna('')` to replace every empty owner name with an empty string. This might not happen to you, though, depending on how you do it!
# 
# * **Hint:** You probably want to do `expand=False` on your extraction to make sure it comes out as a series instead of a dataframe.

# In[21]:


df.head(13)


# In[22]:


df['OWNER'].str.extract(r"(\w*),", expand=False)


# In[ ]:





# ## 14. Save the last name into a new column
# 
# Then check to make sure it exists, and you successfully saved it into the dataframe.

# In[23]:


df['lastname'] = df['OWNER'].str.extract(r"(\w*),", expand=False)


# In[24]:


#df.lastname.isna().value_counts()
#df[df.lastname.isna()]


# # 15. What are the ten most popular last names?

# In[25]:


df.lastname.value_counts().head(10)


# ## 16. What are the most popular licenses for people with the last name Nguyen? Tran? Le?
# 
# Those are the top 3 last names in Vietnam.

# In[26]:


df['LICTYPE'][df.lastname =='NGUYEN'].value_counts().head()


# In[27]:


df['LICTYPE'][df.lastname =='TRAN'].value_counts().head()


# In[28]:


df['LICTYPE'][df.lastname == 'LE'].value_counts().head()


# The background of this [is interesting](https://www.npr.org/2019/05/19/724452398/how-vietnamese-americans-took-over-the-nails-business-a-documentary) and [tragic](https://www.nytimes.com/2015/05/10/nyregion/at-nail-salons-in-nyc-manicurists-are-underpaid-and-unprotected.html).

# ## 17. Now do all of that in one line - most popular licenses for Nguyen, Tran and Le - without using `&`

# In[29]:


df['LICTYPE'][df.lastname.isin(['NGUYEN','TRAN','LE'])].value_counts().head()


# ## 19. Most popular license for anyone with a last name that ENDS in `-ko`
# 
# The answer is not `.str.contains('ko')`, but it isn't necessarily too different.
# 
# * One way involves a `.str.` method that check if a string ends with something,
# * the other way involves a regular expression that has a "end of the string" marker (similar to how we've used `^` for the start of a string before)
# 
# If you're thinking about the latter, I might take a look at [this page](http://www.rexegg.com/regex-quickstart.html) under "Anchors and Boundaries". 

# In[30]:


df.lastname = df.lastname.fillna('None')
df.lastname.isna().value_counts()
df.head()


# In[31]:


df[df['lastname'].str.match(r".*KO$")]


# In[32]:


df['LICTYPE'][df['lastname'].str.match(r".*KO$")].value_counts().head(1)


# In[33]:


#df['LICTYPE'][df.lastname.(r".*ko$")]


# ## 20. Get that as a percentage

# In[34]:


df['LICTYPE'][df['lastname'].str.match(r".*KO$")].value_counts(normalize=True).head(1)*100


# # PART FOUR: LOOKING AT FIRST NAMES

# ## 21. Extract the owner's first name
# 
# First, a little example of how regular expressions work with pandas.

# In[35]:


# Build a dataframe
sample_df = pd.DataFrame([
    { 'name': 'Mary', 'sentence': "I am 90 years old" },
    { 'name': 'Jack', 'sentence': "I am 4 years old" },
    { 'name': 'Anne', 'sentence': "I am 27 years old" },
    { 'name': 'Joel', 'sentence': "I am 13 years old" },
])
# Look at the dataframe
sample_df


# In[36]:


# Given the sentence, "I am X years old", extract digits from the middle using ()
# Anything you put in () will be saved as an output.
# If you do expand=True it makes you a dataframe, but we don't want that.
sample_df['sentence'].str.extract("I am (\d+) years old", expand=False)


# In[37]:


# Save it into a new column
sample_df['age'] = sample_df['sentence'].str.extract("I am (\d+) years old", expand=False)
sample_df.head()


# **Now let's think about how we're going to extract the first names.** Begin by looking at a few full names.

# In[38]:


df['OWNER'].head(12)


# What can you use to find the first name? It helps to say "this is to the left and this is to the right, and I'm going to take anything in the middle."
# 
# Once you figure out how to extract it, you can do a `.head(10)` to just look at the first few.

# In[39]:


#df['OWNER'].str.extract(r",\s?([\w\W\s]*)$").head(10)
df['OWNER'].str.extract(r",\s?(\w*)[\W\w]*$").head(10)


# ## 22. Saving the owner's first name
# 
# Save the name to a new column, `FIRSTNAME`.

# In[40]:


df['FIRSTNAME'] = df['OWNER'].str.extract(r",\s?(\w*)[\W\w]*$")
df.head()


# # 23. Examine everyone without a first name
# 
# I purposefully didn't do a nicer regex in order to have some screwed-up results. **How many people are there without an entry in the first name column?**
# 
# Your numbers might be different than mine.

# In[41]:


df.FIRSTNAME.isna().value_counts()


# What do their names look like?

# In[42]:


df[df.FIRSTNAME.isna()]


# ## 24. If it's a problem, you can fix it (if you'd like!)
# 
# Maybe you have another regular expression that works better with JUST these people? It really depends on how you've put together your previous regex!
# 
# If you'd like to use a separate regex for this group, you can use code like this:
# 
# `df.loc[df.FIRSTNAME.isnull(), 'FIRSTNAME'] = .....`
# 
# That will only set the `FIRSTNAME` for people where `FIRSTNAME` is null.

# In[43]:


#I'm confused... It seems most of the missing first names are because the owner's name is listed as a company. 
# Should the regex change to include them?? 


# In[44]:


#These are some common problems/still-dirty things I noticed in the data. There could be more I am not sure how to remove them


# In[45]:


df[df.FIRSTNAME == 'INC']


# In[46]:


df[df.FIRSTNAME == 'LLC']


# How many empty first names do we have now?

# In[47]:


df[df.lastname == 'None']


# In[48]:


df[df.FIRSTNAME == 'CO']


# In[49]:


df.FIRSTNAME = df.FIRSTNAME.fillna('None')
#For some reason dropna was not working properly -- 
#also there were 82,000 values without a first name so I didn't know if that was too many to drop


# In[50]:


df.FIRSTNAME.isna().value_counts()


# In[51]:


#df[df.lastname.str.contains('&')]


# My code before only worked for people with middle names, but now it got people without middle names, too. Looking much better!

# ## 25. Most popular first names?

# In[52]:


df.FIRSTNAME.value_counts().head(10)
#Noticing "Inc" and "LLC" here so maybe I need to revisit the regex!


# ## 26. Most popular first names for a Cosmetology Operator, Cosmetology Esthetician, Cosmetologist, and anything that seems similar?
# 
# If you get an error about "cannot index vector containing NA / NaN values" remember `.fillna(False)` or `na=False` - if a row doesn't have a license, it doesn't give a `True`/`False`, so we force all of the empty rows to be `False`.

# In[53]:


df.FIRSTNAME[df['LICTYPE'].isin(['Cosmetology Operator', 'Cosmetology Esthetician', 'Cosmetologist'])].value_counts()


# ## 27. Most popular first names for anything involving electricity?

# In[54]:


df.FIRSTNAME[df['LICTYPE'].str.contains('Electric')].value_counts()


# ## 28. Can we be any more obnoxious in this assignment?
# 
# A terrible thing that data analysts are often guilty of is using names to make assumptions about people. Beyond stereotypes involving last names, first names are often used to predict someone's race, ethnic background, or gender.
# 
# And if that isn't bad enough: if we were looking for Python libraries to do this sort of analysis, we'd come across [sex machine](https://github.com/ferhatelmas/sexmachine/). Once upon a time there was Ruby package named sex machine and everyone was like "come on are you six years old? is this how we do things?" and the guy was like "you're completely right I'm renaming it to [gender detector](https://github.com/bmuller/gender_detector)" and the world was Nice and Good again.
# 
# How'd it happen? [On Github, in a pull request!](https://github.com/bmuller/gender_detector/pull/14) Neat, right?
# 
# But yeah: apparently Python didn't get the message.
# 
# The sexmachine package doesn't work on Python 3 because it's from 300 BC, so we're going to use a Python 3 fork with the less problematic name [gender guesser](https://pypi.python.org/pypi/gender-guesser/).
# 
# #### Use `pip` or `pip3` to install gender-guesser.

# In[55]:


get_ipython().system('pip install gender-guesser')


# #### Run this code to test to see that it works

# In[56]:


import gender_guesser.detector as gender

detector = gender.Detector(case_sensitive=False)
detector.get_gender('David')


# In[57]:


detector.get_gender('Jose')


# In[58]:


detector.get_gender('Maria')


# #### Use it on a dataframe
# 
# To use something fancy like that on a dataframe, you use `.apply`. Check it out: 

# In[59]:


df.FIRSTNAME.head()


# In[60]:


#df.dtypes


# In[61]:


#df.FIRSTNAME.apply(lambda name: detector.get_gender(name)).head()
df.FIRSTNAME.apply(lambda name: detector.get_gender(name))


# In[62]:


df.FIRSTNAME.isna().value_counts()


# ## 29. Calculate the gender of everyone's first name and save it to a column
# 
# Confirm by see how many people of each gender we have

# In[63]:


df.FIRSTNAME.apply(lambda name: detector.get_gender(name)).value_counts()


# In[64]:


df['GENDER'] = df.FIRSTNAME.apply(lambda name: detector.get_gender(name))


# In[65]:


df.head()


# ## 30. We like our data to be in tidy binary categories
# 
# * Combine the `mostly_female` into `female` 
# * Combine the `mostly_male` into `male`
# * Replace `andy` (androgynous) and `unknown` with `NaN`
# 
# you can get NaN not by making a string, but with `import numpy as np` and then using `np.nan`.

# In[66]:


import numpy as np


# In[67]:


df.GENDER = df.GENDER.replace('mostly_female', 'female')
#df[df.GENDER == 'mostly_female']


# In[68]:


df.GENDER = df.GENDER.replace('mostly_male', 'male')
#df[df.GENDER == 'mostly_male']


# In[69]:


df.GENDER = df.GENDER.replace('andy', np.nan)
df.GENDER = df.GENDER.replace('unknown', np.nan)
#df[df.GENDER == 'andy']


# ## 31. Do men or women have more licenses? What is the percentage of unknown genders?

# In[70]:


df.GENDER.value_counts(dropna=False)


# In[71]:


df.GENDER.value_counts(dropna=False, normalize=True)*100


# ## 32. What are the popular unknown- or ambiguous gender first names?
# 
# Yours might be different! Mine is a combination of actual ambiguity, cultural bias and dirty data.

# In[72]:


df.FIRSTNAME[df.GENDER.isna()].value_counts().head(10)


# ## 33. Manually check a few, too 
# 
# Using [a list of "gender-neutral baby names"](https://www.popsugar.com/family/Gender-Neutral-Baby-Names-34485564), pick a few names and check what results the library gives you.

# In[73]:


#Flynn, Dakota, Alex
df.GENDER[df.FIRSTNAME.isin(['ALEX', 'FLYNN','DAKOTA', 'CODY'])].value_counts()


# ## 34. What are the most popular licenses for men? For women?

# In[74]:


df.LICTYPE[df.GENDER == 'male'].value_counts().head(10)


# In[75]:


df.LICTYPE[df.GENDER == 'female'].value_counts().head(10)


# ## 35. What is the gender breakdown for Property Tax Appraiser? How about anything involving Tow Trucks?
# 
# If you're in need, remember your good friend `.fillna(False)` to get rid of NaN values, or `.na=False` with `.str.contains`.

# In[76]:


df.GENDER[df.LICTYPE == 'Property Tax Appraiser'].value_counts()


# In[77]:


df.GENDER[df.LICTYPE.str.contains('Tow Truck')].value_counts()


# (By the way, what are those tow truck jobs?)

# In[78]:


df.LICTYPE[df.LICTYPE.str.contains('Tow Truck')].value_counts()


# ## 33. Graph them!
# 
# And let's **give them titles** so we know which is which.

# In[79]:


df.LICTYPE[df.LICTYPE.str.contains('Tow Truck')].value_counts().plot(kind='barh')


# In[ ]:





# ## 34. Calcuate the supposed gender bias for profession
# 
# I spent like an hour on this and then realized a super easy way to do it. Welcome to programming! I'll do this part for you.

# In[80]:


# So when you do .value_counts(), it gives you an index and a value
df[df['GENDER'] == 'male'].LICTYPE.value_counts().head()


# We did `pd.concat` to combine dataframes, but you can also use it to combine series (like the results of `value_counts()`). If you give it a few `value_counts()` and give it some column names it'll make something real nice.

# In[81]:


# All of the values_counts() we will be combining
vc_series = [
    df[df['GENDER'] == 'male'].LICTYPE.value_counts(),
    df[df['GENDER'] == 'female'].LICTYPE.value_counts(),
    df[df['GENDER'].isnull()].LICTYPE.value_counts()
]
# You need axis=1 so it combines them as columns
gender_df = pd.concat(vc_series, axis=1)
gender_df.head()


# In[82]:


# Turn "A/C Contractor" etc into an actual column instead of an index
gender_df.reset_index(inplace=True)
gender_df.head()


# In[83]:


# Rename the columns appropriately
gender_df.columns = ["license", "male", "female", "unknown"]
# Clean up the NaN by replacing them with zeroes
gender_df.fillna(0, inplace=True)
gender_df.head()


# ## 35. Add new columns for total licenses, percent known (not percent unknown!), percent male (of known), percent female (of known)
# 
# And replace any `NaN`s with `0`.

# In[84]:


gender_df['total_licenses'] = gender_df.male + gender_df.female + gender_df.unknown
gender_df.head()


# In[85]:


gender_df['pct_known'] = ((gender_df.male + gender_df.female) / gender_df.total_licenses) * 100
gender_df.head()


# In[86]:


gender_df['pct_male_known'] = (gender_df.male / (gender_df.male + gender_df.female)) * 100
gender_df.head()


# In[87]:


gender_df['pct_female_known'] = (gender_df.female / (gender_df.male + gender_df.female)) * 100
gender_df.head()


# ## 35. What 10 licenses with more than 2,000 people and over 75% "known" gender has the most male owners? The most female?

# In[88]:


gender_df[(gender_df.total_licenses > 2000) & (gender_df.pct_known > 75)].sort_values(by='male', ascending=False).head(10)


# In[89]:


gender_df[(gender_df.total_licenses > 2000) & (gender_df.pct_known > 75)].sort_values(by='female', ascending=False).head(10)


# ## 36. Let's say you have to call a few people about being in a profession dominated by the other gender. What are their phone numbers?
# 
# This will involve doing some research in one dataframe, then the other one. I didn't put an answer here because I'm interested in what you come up with!

# In[90]:


#gender_df.license[(gender_df.pct_male_known > gender_df.pct_female_known) | (gender_df.pct_female_known > gender_df.pct_male_known)].head(10)

gender_df['LICTYPE'] = gender_df.license[(gender_df.pct_male_known > gender_df.pct_female_known) | (gender_df.pct_female_known > gender_df.pct_male_known)]
gender_df

#I was trying to calculate the difference between percentage of occupation, and then sort by the highest difference
#But I kept getting value errors


# if gender_df.pct_male_known.all() > gender_df.pct_female_known.all():
#     diff = gender_df.pct_male_known - gender_df.pct_female_known
# elif gender_df.pct_male_known.all() < gender_df.pct_female_known.all():
#     diff = gender_df.pct_female_known - gender_df.pct_male_known

#     gender_df['diff'] = diff

# gender_df.head()
#gender_df.license[diff1].sort_values(dropna=True)


# In[91]:


#df[(df['LICTYPE'] == gender_df['LICTYPE'])]
# ValueError: Can only compare identically-labeled Series objects   
   
   
  


# ## Okay, let's take a break for a second.
# 
# We've been diving pretty deep into this gender stuff after an initial "oh but it's not great" kind of thing.
# 
# **What issues might come up with our analysis?** Some might be about ethics or discrimination, while some might be about our analysis being misleading or wrong. Go back and take a critical look at what we've done since we started working on gender, and summarize your thoughts below.

# In[92]:


#The gender detector package still seems flawed, especially considering names that are "gender neutral" are often viewed as
#either male or female depending on more traditional connotations. Also a number of names are unknown because they are not
#conventional names commonly found in the United States. For eg, Jose and Juan are there but Trang etc. are not.
#There is also lots and lots of unknown data re: professions itself, so it may not be giving us an accurate portrayal of gender and labour breakdowns.




# If you found problems with our analysis, **how could we make improvements?**

# In[93]:


#Either try to find the missing data with documentation/reaching out to the source, or filter with only known values and call it a sample ratehr than accurate data? 


# In[ ]:





# ## PART FIVE: Violations
# 
# ### 37. Read in **violations.csv** as `violations_df`, make sure it looks right

# In[94]:


violations_df = pd.read_csv("violations.csv")
violations_df


# ### 38. Combine with your original licenses dataset dataframe to get phone numbers and addresses for each violation. Check that it is 90 rows, 28 columns.

# In[95]:


merged = violations_df.merge(df, how='left',
                            left_on= 'licenseno', 
                            #left_on= 'name'
                            right_on='LICNUMBER')
                            #right_on='OWNER')
#merged = pd.set_option('display.max_colwidth')
merged.head()


# In[96]:


#There are 115 rows and 31 columns (the 3 extra columns are the ones we added in, I think) but there were 115 columns in the violations df, so I just left it?


# ## 39. Find each violation involving a failure with records. Use a regular expression.

# In[97]:


violations_df.dtypes


# In[98]:


#violations_df.str.extract(r"[\w\W]+fail[\w\W]*record")
violations_df[violations_df.basis.str.contains(r"fail")]


# ## 40. How much money was each fine? Use a regular expression and .str.extract
# 
# Unfortunately large and helpful troubleshooting tip: `$` means "end of a line" in regex, so `.extract` isn't going to accept it as a dollar sign. You need to escape it by using `\$` instead.

# In[99]:


violations_df.order.str.extract(r"\$([\d\W]*)").head(10)


# ## 41. Clean those results (no commas, no dollar signs, and it should be an integer) and save it to a new column called `fine`
# 
# `.replace` is for *entire cells*, you're interested in `.str.replace`, which treats each value like a string, not like a... pandas thing.
# 
# `.astype(int)` will convert it into an integer for you.

# In[100]:


violations_df['fine'] = violations_df.order.str.extract(r"\$([\d\W]*)")
violations_df['fine'] = violations_df['fine'].str.replace('[,.]','')
violations_df['fine'] = violations_df['fine'].fillna('None')
violations_df['fine'] = violations_df['fine'].astype(int, errors='ignore')
violations_df.head(20)


# ## 42. Which orders results in the top fines?

# In[101]:


violations_df.sort_values(by='fine',ascending=False).head(20)


# ## 43. Are you still here???
# 
# I'm sure impressed.

# In[102]:


#Just barely.

