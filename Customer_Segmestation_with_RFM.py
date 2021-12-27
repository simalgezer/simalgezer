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

