from regexes import *
from utils import read_tweets

import os
import re
import string
from tqdm import tqdm
from itertools import chain
from collections import Counter, defaultdict
import json

DATA_FOLDER = os.path.join('data', 'english_1M_tagged')
DICT_PATH = os.path.join('data', '_15M_sample_words.txt')  # This is from Sam Liu


def filter_case(counter):
    # count title case as lower case, and only
    # distinguish between upper vs lower case

    counter = dict(counter)
    for form in list(counter.keys()):
        if form.istitle():
            word = form.lower()
            if word in counter:
                counter[word] += counter[form]
            else:
                counter[word] = counter[form]

            del counter[form]

        elif not (form.isupper() or form.islower()):
            del counter[form]

    return counter


def count_tokens(tweet_dict):
    text = chain.from_iterable(tweet_dict.values())
    counter = Counter()
    text = filter(lambda tok: tok.pos not in {'#', '@', 'U', 'E'} and tok.form.isalpha(), text)
    forms = [tok.form for tok in text]
    counter = Counter(forms)

    return filter_case(counter)


# need to create lengthening map from english_1M data
# e.g. heroicaly -> heroically
def get_normal_map(counter):
    counts = defaultdict(Counter)
    for word, n in tqdm(counter.items()):
        if not word.isalpha():
            continue

        word = word.lower()
        if lengthened_word_re.match(word):
            short = two_char_re.sub(r'\1', word)
            counts[short][word] = n

    mapping = {}
    for short, n in counts.items():
        forms = n.most_common()
        canon = forms[0][0]
        if short != canon and not three_char_re.search(canon):
            mapping[short] = canon

    return mapping


def count_caps(counter, normal_map):
    counts = defaultdict(lambda: defaultdict(int))

    for word, count in counter.items():
        form = word.lower()

        if lengthened_word_re.match(form):
            form = two_char_re.sub(r'\1', form)
            if form in normal_map:
                form = normal_map[form]

        if len(form) > 2:
            entry = counts[form]
            if word.isupper():
                entry['upper'] += 1
            else:
                entry['non-upper'] += 1

    return counts


def load_15M_dict(dict_path):
    counter = {}
    with open(dict_path, encoding='utf-8') as infile:
        for line in tqdm(infile):
            line = line.split('\t')
            word = line[0]
            if word.isalpha():
                counter[word] = int(line[1])

    return counter


def get_counts(counter, dict_path, normal_map):
    counter_15M = load_15M_dict(dict_path)
    return count_caps(Counter(counter) + Counter(counter_15M), normal_map)


def is_meaningful(word, counts):
    word = word.lower()
    entry = counts[word]
    if entry['upper'] > entry['non-upper']:
        return False
    return True


def main():
    pos_data = defaultdict(lambda: defaultdict(int))
    seq_data = {}
    count_data = {}
    percent_data = {}

    for tweet_id, tok_list in tqdm(tweet_dict.items()):
        tweet_id = int(tweet_id)

        p_meaningful = n_meaningful = n_caps = 0
        pos_list = []

        tok_list = list(filter(lambda x: x.pos not in {'#', '@', 'U', 'E', ','} and len(x.form) > 2, tok_list))
        if not tok_list:
            continue

        # find longest capitalized sequence
        this_string = ' '.join(tok.form for tok in tok_list)
        sequences = []
        for m in caps_seq_re.finditer(this_string):
            sequences.append(m.group(1))


        if sequences:
            longest = max(sequences, key=lambda x: len(x.split()))

            # hack to exclude cases like LOL I'
            exclude = set(string.punctuation)
            longest = ''.join(c for c in longest if c not in exclude)
            if all(len(w) > 1 for w in longest.split()):
                seq_data[tweet_id] = len(longest.split())


        # find capitalized parts of speech
        for tok in tok_list:
            word = tok.form

            if word.isupper():
                n_caps += 1

                if lengthened_word_re.match(word):
                    normal = two_char_re.sub(r'\1', word)
                    if normal.lower() in normal_map:
                        normal = normal_map[normal.lower()].upper()

                    word = normal

                if is_meaningful(word, counts):
                    # increment count for pos that was capitalized
                    pos_data[tweet_id][tok.pos] += 1
                    n_meaningful += 1

        p_meaningful = n_meaningful / len(tok_list)
        count_data[tweet_id] = n_meaningful
        percent_data[tweet_id] = p_meaningful * 100


    with open('1M_pos.json', 'w') as outfile:
        json.dump(pos_data, outfile)

    with open('1M_seqwith1.json', 'w') as outfile:
        json.dump(seq_data, outfile)

    with open('1M_count.json', 'w') as outfile:
        json.dump(count_data, outfile)

    with open('1M_percent.json', 'w') as outfile:
        json.dump(percent_data, outfile)


# main part is here
tweet_dict = read_tweets(DATA_FOLDER)
counter = count_tokens(tweet_dict)
normal_map = get_normal_map(counter)
# counts = get_counts(counter, DICT_PATH, normal_map)

# with open('1M_15M_counts.json', 'w') as outfile:
    # json.dump(counts, outfile)

with open('normal_map.json', 'w') as outfile:
    json.dump(normal_map, outfile)
# main()
