# usage: build_dictionary.py <input dir> <output name (.json)>
# input directory contains text files, where each row has the format
#   word <tab> count

import os
import sys
import json
import time

dictionary = {}

input_dir = sys.argv[1]
output_name = sys.argv[2]

filenames = [fn for fn in os.listdir(input_dir)]

for fn in filenames:
    print('processing %s' % fn)

    start = time.time()

    with open(os.path.join(input_dir, fn), encoding='utf-8') as infile:
        for l in infile:
            word, count = l.split('\t')
            dictionary[word] = int(count.strip())
    
    print('\tdone processing %s, took %.2f' % (fn, (time.time()-start)))
    

with open(output_name, 'w', encoding='utf-8') as outfile:
    json.dump(dictionary, outfile)