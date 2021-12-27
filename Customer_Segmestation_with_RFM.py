#Importing libraries & data reading 
import datetime as dt
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

df_ = pd.read_excel("/Users/simalgezer/Desktop/online_retail_II.xlsx", sheet_name="Year 2010-2011")
df = df_.copy()

df.describe().T
df.shape

df.isnull().sum()
df.dropna(inplace=True)
df.shape

df = df[~df["Invoice"].str.contains("C", na=False)]

df['TotalPrice']=df['Price']*df['Quantity']
df.head()

#Calculating RFM metrics
df["InvoiceDate"].max()
today_date = dt.datetime(2010, 12, 11)

rfm = df.groupby('Customer ID').agg({'InvoiceDate': lambda date: (today_date - date.max()).days,
                                     'Invoice': lambda num: num.nunique(),
                                     'TotalPrice': lambda TotalPrice: TotalPrice.sum()})

rfm.head()
rfm.columns = ['recency', 'frequency', 'monetary']
rfm.head()
rfm.describe().T

rfm = rfm[rfm["monetary"] > 0]

#Assigning RFM Scores & mapping segments
 rfm["recency_score"] = pd.qcut(rfm['recency'], 5, labels=[5, 4, 3, 2, 1])
rfm["frequency_score"] = pd.qcut(rfm['frequency'].rank(method="first"), 5, labels=[1, 2, 3, 4, 5])
rfm["monetary_score"] = pd.qcut(rfm['monetary'], 5, labels=[1, 2, 3, 4, 5])
rfm["RFM_SCORE"] = (rfm['recency_score'].astype(str) +
                    rfm['frequency_score'].astype(str))

rfm.describe().T
rfm.head()

seg_map = {
    r'[1-2][1-2]': 'hibernating',
    r'[1-2][3-4]': 'at_Risk',
    r'[1-2]5': 'cant_loose',
    r'3[1-2]': 'about_to_sleep',
    r'33': 'need_attention',
    r'[3-4][4-5]': 'loyal_customers',
    r'41': 'promising',
    r'51': 'new_customers',
    r'[4-5][2-3]': 'potential_loyalists',
    r'5[4-5]': 'champions'
}
rfm['segment'] = rfm['RFM_SCORE'].replace(seg_map, regex=True)
rfm.head()

#Reviews about some of the segments

#Below, frequency is high while recency is low in these two groups. 
#Remarketing studies can be done (ex. email reminder, providing a promotional code).

rfm[rfm['segment']=='cant_loose']
rfm[rfm['segment']=='at_Risk']

#Below, both these groups can be categorized as "newcomers". 
#Frequency score of these customers can be increased by cross-selling and up-selling.

rfm[rfm['segment']=='new_customers']
rfm[rfm['segment']=='promising']

# Below, these groups are those who know the brand and shop regularly.
# Promotions and special discounts can be provided to keep them satisfied.
# Communication channels can be kept active (email, sms, etc.).

rfm[rfm['segment']=='champions']
rfm[rfm['segment']=='potential_loyalists']
