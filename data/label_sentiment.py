# label_sentiment.py --input=<text file of tweets>

import sys
import os
import re
import csv
import codecs
import numpy as np
import pandas as pd
from tqdm import tqdm
from collections import defaultdict
from rankings.load import NRC, SEMEVAL
from itertools import islice
from emoticons import Emoticon_RE, analyze_tweet

HASHTAG_PATTERN = re.compile(r'#\w+')

# merge the 3 different rankings 
hashtag_dict = {}
nrc_keys = set(NRC.keys())
sem_keys = set(SEMEVAL.keys())
intersection = (nrc_keys & sem_keys)
for tag in nrc_keys | sem_keys:
    if tag in intersection:
        average = np.mean([NRC[tag], SEMEVAL[tag]])
        hashtag_dict[tag] = average
    else:
        try:
            score = NRC[tag]
        except KeyError:
            score = SEMEVAL[tag]
        hashtag_dict[tag] = score
    
# score_dict = {**hashtag_dict}
score_dict = dict((v, k) for k, v in hashtag_dict.iteritems())
hashtag_set = set(hashtag_dict.keys())


def clean(tweet):
	tweet = strip_emoticons(tweet)
	return strip_hashtags(tweet).strip()

	
def strip_hashtags(tweet):
	return HASHTAG_PATTERN.sub(' ', tweet)


def strip_emoticons(tweet):
	for m in Emoticon_RE.finditer(tweet):
		tweet = tweet.replace(m.group(0), ' ')
	return tweet
	
    
def find_hashtags(tweet):
    return [t for t in HASHTAG_PATTERN.findall(tweet) if t in hashtag_set]
    
    
def process_hashtags(tweet):
    tags = find_hashtags(tweet)
    if tags:
        tags.sort()
        scores = [score_dict[t] for t in tags]
        return [' '.join(tags), np.mean(scores), np.std(scores)]
    return False
    

def process_emoticons(tweet):
	sentiment = analyze_tweet(tweet)
	if sentiment == 'HAPPY' or sentiment == 'SAD':
		emoticons = [m.group(0) for m in Emoticon_RE.finditer(tweet)]
		if len(emoticons) != 1 or emoticons[0] != ':)':
			sentiment = 'positive' if sentiment == 'HAPPY' else 'negative'
			return [' '.join(emoticons), sentiment]
	return False
    
    
def process_tweet(tweet, label):
    # each tweet begins with a #tweet_id
    id, _, tweet = tweet.partition(' ')
    id = int(id[1:])
    
    if label == 'hashtags':
        result = process_hashtags(tweet)
    elif label == 'emoticons':
        result = process_emoticons(tweet)
        
    if result:
        return [id, tweet] + result
    return False
    
        
def main():
    in_file = sys.argv[1]

    with codecs.open(in_file, 'r', 'utf-8') as f:
        lines = f.readlines()
   
    for label in ['hashtags', 'emoticons']:
        if label == 'hashtags':
            columns = ['tweet_id', 'tweet', 'tags', 'sentiment_score', 'standard_deviation']
        else:
            columns = ['tweet_id', 'tweet', 'emoticons', 'sentiment']
		
        out_name = in_file[:-4] + '_sentiment_%s.csv' % label
        rows = []
        
        for line in tqdm(lines):
            result = process_tweet(line, label)
            if result:
                rows.append(result)
        
        df = pd.DataFrame(rows, columns=columns)
        if label == 'hashtags':
            df = df.sort_values(by='standard_deviation', ascending=False)
        df.to_csv(out_name, encoding='utf-8')

		
if __name__ == '__main__':
    main()
