import pandas as pd
import json
import sys
import os

SENTIMENT_GENDER_DATA = os.path.join('data', '1M_sentiment_gender.csv')
FOLDER = 'output'
SEQ_DATA = '1M_seqwith1.json'   # longest meaningfully capitalized sequence
COUNT_DATA = '1M_count.json'  # raw counts of meaningfully capitalized words
PERCENT_DATA = '1M_percent.json'  # percentage of tweet that's meaningfully capitalized


df = pd.read_csv(SENTIMENT_GENDER_DATA, encoding='utf-8', index_col=0)

for name, data in [('seq', SEQ_DATA), ('count', COUNT_DATA), ('percent', PERCENT_DATA)]:
    with open(os.path.join(FOLDER, data)) as infile:
        data = json.load(infile)
    
    num_data = {}
    for k, v in data.items():
        num_data[int(k)] = v
    
    df[name] = pd.Series(num_data)
    
# print(df)
# df = df.dropna(axis=0)

df = df.fillna(value=0)
df.to_csv('1M_sentiment_gender_joined.csv', encoding='utf-8')
