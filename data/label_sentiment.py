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
from itertools import islice
from emoticons import Emoticon_RE, analyze_tweet

HASHTAG_PATTERN = re.compile(r'#\w+')


def clean(tweet):
	tweet = strip_emoticons(tweet)
	return strip_hashtags(tweet).strip()


def strip_hashtags(tweet):
	return HASHTAG_PATTERN.sub(' ', tweet)


def strip_emoticons(tweet):
	for m in Emoticon_RE.finditer(tweet):
		tweet = tweet.replace(m.group(0), ' ')
	return tweet


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

    result = process_emoticons(tweet)

    if result:
        return [id, tweet] + result
    return False


def main():
    in_file = sys.argv[1]

    with codecs.open(in_file, 'r', 'utf-8') as f:
        lines = f.readlines()

        columns = ['tweet_id', 'tweet', 'emoticons', 'sentiment']

        out_name = in_file[:-4] + '_sentiment_%s.csv' % label
        rows = []

        for line in tqdm(lines):
            result = process_tweet(line)
            if result:
                rows.append(result)

        df = pd.DataFrame(rows, columns=columns)
        df.to_csv(out_name, encoding='utf-8')


if __name__ == '__main__':
    main()
