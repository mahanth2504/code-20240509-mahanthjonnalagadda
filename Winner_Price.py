
# Import library
import pandas as pd
import numpy as np

#read tsv file
url='https://github.com/mahanth2504/code-20240509-mahanthjonnalagadda/raw/main/interview_analysis_molecule_x_10mg_v1.tsv'
data=pd.read_table(url)

#data manipulation
df=data[['contract_id','sku','participants','participants_price']]

#split the participants columns with delimiter to object
name=df["participants"].str.split("|",expand=True)

#split the participants_price columns with delimiter and Converting price column to numeric
price = df["participants_price"].str.split("|",expand=True).astype(float)

#joining df and name dataframes
bidder_name=df.drop(columns=['participants','participants_price']).join(name)

#stacking name df
bid_name=bidder_name.set_index(['contract_id','sku']).stack().reset_index()
bid_name.rename(columns={'level_2':'partic_no',0:'participants'},inplace=True)

#joining df and price dataframes
bidder_price=df.drop(columns=['participants','participants_price']).join(price)

#stack price dataframe
bid_price=bidder_price.set_index(['contract_id','sku']).stack().reset_index()
bid_price.rename(columns={'level_2':'partic_no',0:'price'},inplace=True)

# merge required dataframes to get final bidder details
bidder_details=pd.merge(bid_name,bid_price,on=['contract_id','sku','partic_no'])

# Grouping by contract id and price and finding the row with the minimum price for each group
winner_bid=bidder_details.loc[bidder_details.groupby('contract_id')['price'].idxmin()]

# Displaying the result
print(winner_bid[['contract_id','sku','participants','price']])

# export to tsv file
winner_bid.to_csv('winner_bid.tsv',sep="\t")
