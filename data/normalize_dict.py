# usage: normalize_dict.py <dictionary file (.json)>

import os
import sys
import json
import re
from collections import defaultdict, Counter


lengthened_word_re = re.compile(r"""
    ^                   # string start
    [A-Za-z-]*          # 0 or more characters
    ([A-Za-z-])\1{1,}   # 2 or more of the same character
    [A-Za-z-]*          # 0 or more characters
    $                   # string end
    """, re.VERBOSE)


dictionary_name = sys.argv[1]
dir_name = os.path.dirname(os.path.abspath(__file__))
out_name = os.path.join(dir_name, os.path.basename(dictionary_name))

    
two_char_re = re.compile(r'([A-Za-z-])\1{1,}')  # sequence of 2 or more repeated
three_char_re = re.compile(r'([A-Za-z-])\1{2,}')  # sequence of 3 or more repeated
    
with open(dictionary_name) as f:
    dictionary = json.load(f)


titles = {word for word in dictionary.keys() if word.istitle()}
# convert titles to lowercase in the dictionary
for title in titles:
    word = title.lower()
    if word in dictionary:
        # add to count of already-existing lowercase word
        dictionary[word] += dictionary[title]
    else:
        dictionary[word] = dictionary[title]
        
    del dictionary[title]
    

counts = defaultdict(Counter)
    
for word, num in dictionary.items():
    # only consider fully uppercase or lowercase words
    if (word.isupper() or word.islower()) and lengthened_word_re.match(word):
        # replace all cases of 2 or more repeated characters
        # with a single character
        normal = two_char_re.sub(r'\1', word)
        counts[normal][word] = num
        
        # add the normalized form to the counts too
        if normal not in counts[normal] and normal in dictionary:
            counts[normal][normal] = dictionary[normal]

            
normalized_map = {}  # mapping of normalized to canon form (helo, hello)
for normal, counter in counts.items():
    forms = counter.most_common()
    canon = forms[0]
    lengthened = forms[1:]
    
    if not lengthened:
        continue
        
    if not three_char_re.search(canon[0]) and normal != canon[0] and canon[1] > 1:
        normalized_map[normal.lower()] = canon[0].lower()
    
    # delete lengthened forms from original dictionary
    for word, num in lengthened:
        del dictionary[word]

    dictionary[canon[0]] += sum(x[1] for x in lengthened)
    
    
with open(out_name + '.normalized', 'w', encoding='utf-8') as f:
    json.dump(dictionary, f)

with open(out_name + '.lengthening', 'w', encoding='utf-8') as f:
    json.dump(normalized_map, f)
