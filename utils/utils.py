import sys
import os
import re
import json
from collections import Counter
from pandas import read_csv
from tqdm import tqdm
from twokenize import tokenize
from CMUTweetTagger import runtagger_parse
from regexes import lengthened_word_re, two_char_re


# kwargs must be passed in the form of a dict
def csv2df(csvfile, **kwargs):
    return read_csv(csvfile, encoding='utf-8', low_memory=False, **kwargs)

    
def clean_lines(series):
    return series.map(lambda x: x.replace('\n', ' ').replace('\r', ''))

    
def write2txt(series, out_name):
    with open(out_name, 'w', encoding='utf-8') as outfile:
        for l in series:
            outfile.write(l + '\n')
       
       
def is_lengthened(word):
    if lengthened_word_re.match(word):
        return True
    return False
    

def load_dict(filename):
    with open(filename, encoding='utf-8') as f:
        return json.load(f)
        
        
def load_combined():
    google_path = os.path.join('dicts', 'googlebooks_dictionary.json')
    twitter_path = os.path.join('dicts', 'twitter_dictionary.json.normalized')
    return Counter(load_dict(google_path)) + Counter(load_dict(twitter_path))
    
    
class Token:
    def __init__(self, line):
        line = line.split()
        self.form = line[1]
        self.pos = line[3]
        
    def __repr__(self):
        return '({}, {})'.format(self.form, self.pos)
        
        

# folder must contain .predict files output by TweeboParser
# for each tweet, the first token is the tweet id
# return a dictionary, where each entry represents a tweet
# keys are tweet ids and values are lists of Tokens 
def read_tweets(folder):
    tweet_dict = {}
    for fn in tqdm(os.listdir(folder)):
        if fn.endswith('.txt.predict'):
            content = ''
            with open(os.path.join(folder, fn), encoding='utf-8') as infile:
                content = infile.read()
            
            for tweet in content.split('\n\n'):
                tweet = tweet.split('\n')
                if not len(tweet) > 2:
                    continue
                
                id = tweet[0].split('\t')[1][1:]
                text = [Token(line) for line in tweet[1:]]
                tweet_dict[id] = text
                    
    return tweet_dict 