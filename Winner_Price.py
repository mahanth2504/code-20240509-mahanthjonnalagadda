#!/usr/bin/env python
# coding: utf-8

# In[3]:


# Import library
import pandas as pd
import numpy as np


# In[202]:


#read tsv file
url='https://github.com/mahanth2504/code-20240509-mahanthjonnalagadda/raw/main/interview_analysis_molecule_x_10mg_v1.tsv'
data=pd.read_table(url)


# In[203]:


#data manipulation
df=data[['contract_id','sku','participants','participants_price']]


# In[205]:


#split the participants columns with delimiter to object
name=df["participants"].str.split("|",expand=True)


# In[206]:


#split the participants_price columns with delimiter and Converting price column to numeric
price = df["participants_price"].str.split("|",expand=True).astype(float)


# In[207]:


#joining df and name dataframes
bidder_name=df.drop(columns=['participants','participants_price']).join(name)


# In[208]:


#stacking name df
bid_name=bidder_name.set_index(['contract_id','sku']).stack().reset_index()
bid_name.rename(columns={'level_2':'partic_no',0:'participants'},inplace=True)


# In[209]:


#joining df and price dataframes
bidder_price=df.drop(columns=['participants','participants_price']).join(price)


# In[210]:


#stack price dataframe
bid_price=bidder_price.set_index(['contract_id','sku']).stack().reset_index()
bid_price.rename(columns={'level_2':'partic_no',0:'price'},inplace=True)


# In[211]:


# merge required dataframes to get final bidder details
bidder_details=pd.merge(bid_name,bid_price,on=['contract_id','sku','partic_no'])


# In[212]:


# Grouping by contract id and price and finding the row with the minimum price for each group
winner_bid=bidder_details.loc[bidder_details.groupby('contract_id')['price'].idxmin()]


# In[213]:


# Displaying the result
print(winner_bid[['contract_id','sku','participants','price']])


# In[215]:


# export to tsv file
winner_bid.to_csv('winner_bid.tsv',sep="\t")


# In[ ]:




