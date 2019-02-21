# usage: python get_english_1M.py <path to English_1M.tsv>

import os
import re
import sys
import pandas as pd
import numpy as np
import twitter_api
from twitter.error import TwitterError


in_file = sys.argv[1]
pairs_re = re.compile(r'([a-z ]+)=([A-Za-z0-9 ]+)')

    
def get_tweet(row):
    id = row['TweetID']
    try:
        tweet = twitter_api.api.GetStatus(id)
        print('retrieving tweet for ID %d' % int(id))
        return tweet
    except TwitterError:
        return np.NaN
        

def load_data():
    dfs = []
    with open(data_path) as infile:
        df = pd.DataFrame([dict(pairs_re.findall(l)) for l in infile])
        df = df.rename(columns={'id': 'TweetID'})
        df.to_csv(FILENAME[:-4] + '.csv', encoding='utf-8')
            
    return df
    

def get_info(s):
    try:
        fields = {'Text': s.text, 'Retweeted': s.retweeted, 'Handle': s.user.screen_name}
    except AttributeError:
        fields = {'Text': np.NaN, 'Retweeted': np.NaN, 'Handle': np.NaN}
    
    return pd.Series(fields)
    
    
def populate_tweets(df):
    split_dfs = np.array_split(df, 450)  # split dataframe into 450 chunks
    for i, df_chunk in enumerate(split_dfs):
        status = df_chunk.apply(get_tweet, axis=1)
        new = status.apply(get_info)
        result = pd.concat([df_chunk, new], axis=1)
        # save result to disk
        result.to_csv('English_1M_%d.csv' % i, encoding='utf-8')

        
data = load_data()
populate_tweets(data)
