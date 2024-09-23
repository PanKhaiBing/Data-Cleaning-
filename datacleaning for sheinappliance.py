# Removing duplicate rows
# Combine two columns ('goods-title-link' and 'goods-title-link--jump')
# Rename columns and removing all the symbol for calculation purpose
# Replace NaN to 0 for 'discount' and 'qty_sold'
# Changing the data type for 'discount' and 'qty_sold' from object to int

import pandas as pd
import re

df = pd.read_csv(r'C:\Users\cando\OneDrive\Desktop\Workspaces\Data Cleaning\Shein Appliance\sheinappliance.csv')

def goods_rename(name):
    name = name.lower()
    name = name.replace('pcs','').replace('pc','').replace('unbeatablesale','').strip()
    return name


# Dirty data before cleaning
print('Data before cleaning:')
print(df)
print('\n')

print(df.info())
print('\n')

print(f'Duplicated rows: {df.duplicated().sum()}')
print('\n')

# Remove duplicated rows
df.drop_duplicates(inplace=True)

# Combinining 'goods-title-link' and 'goods-title-link--jump', shortening the 'goods_name'  
# And make it more concise with 'goods_rename' function
if 'goods-title-link' in df.columns:
    df['goods-title-link'] = df['goods-title-link'].fillna(df['goods-title-link--jump'])
    df[['goods_name', 'goods_name2', 'unuse_column']] = df['goods-title-link'].str.split(pat=',', n=2, expand=True)
    df['goods_name'] = df['goods_name'].fillna('') + df['goods_name2'].fillna('')
    df['goods_name'] = df['goods_name'].apply(goods_rename)
    df.drop(columns=['unuse_column', 'goods_name2', 'goods-title-link'], inplace=True)

# Changing the 'k' to 1000, rename column and fill NaN with 0
if 'selling_proposition' in df.columns:
    def convert_k(value):
        if 'k' in str(value):
            num = str(value).replace('k',' ')
            return int(float(num)*1000)
        return value
    df['selling_proposition'] = df['selling_proposition'].str.replace('+ sold recently', ' ')
    df['selling_proposition'] = df['selling_proposition'].apply(convert_k)
    df.rename(columns={'selling_proposition':'qty_sold'}, inplace=True)
    df['qty_sold'] = df['qty_sold'].fillna(0).astype(int)


# Remove symbol and fill NaN with 0
if 'discount' in df.columns:
    df['discount'] = df['discount'].str.replace('%', '')
    df['discount'] = df['discount'].fillna(0).astype(int)

# Remove symbol, changing column's dtype and rename the column
if 'price' in df.columns:
    df['price'] = df['price'].str.replace('$', '')
    df['price'] = pd.to_numeric(df['price'], errors='coerce')
    df['price'] = df['price'].round()
    df.rename(columns={'price':'price_usd'}, inplace=True)

# Remove words and rename column
if 'rank-sub' in df.columns:
    df['rank-sub'] = df['rank-sub'].str.replace('in', '')
    df.rename(columns={'rank-sub':'categories'}, inplace=True)

# Remove words and rename column
if 'rank-title' in df.columns:
    df['rank-title'] = df['rank-title'].str.replace('Best Sellers', '').str.replace('#', '')
    df.rename(columns={'rank-title':'ranking'}, inplace=True)

# Drop unuse column and rearrange the sequences of the column
df.drop(['goods-title-link--jump href', 'goods-title-link--jump'], axis=1, inplace=True)
df = df.reindex(columns=['goods_name'] + list(df.columns[:-1]))

# Data after cleaning
print('Data after cleaning:')
print(df)
print(df.info())


