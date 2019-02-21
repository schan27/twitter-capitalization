# usage: python process_twitter.py <dir> <output_name>
#
# counts the words in all text files in <dir>, outputs a file <output_name>
# where each line has the following format:
#   word <tab> count

from nltk.tokenize import TweetTokenizer
import os
import sys
import time
import preprocessor as p
import pickle
from collections import Counter
from multiprocessing import Pool, freeze_support

LOG = 'log.txt'
dir_name = sys.argv[1]
output_name = sys.argv[2]

filenames = [fn for fn in os.listdir(dir_name) if fn.endswith('.txt')]
tokenizer = TweetTokenizer(preserve_case=True, reduce_len=False)
p.set_options(p.OPT.URL, p.OPT.EMOJI, p.OPT.MENTION, p.OPT.SMILEY, p.OPT.RESERVED)


try:
    os.remove(LOG)
except OSError:
    pass
    
    
def process(fn):
    print('processing %s' % fn)
    
    counter = Counter()
    
    start = time.time()
    with open(os.path.join(dir_name, fn), encoding='utf-8') as infile:
        for line in infile:
            try:
                line = p.clean(line)
                toks = tokenizer.tokenize(line)
                counter.update(Counter(toks))
            except Exception as e:
                # something's wrong with the sentence, write error to log
                # and just continue
                
                with open(LOG, 'a', encoding='utf-8') as logfile:
                    logfile.write('Error processing sentence:\n')
                    logfile.write('\t' + line + '\n')
                    logfile.write(str(e))
                
                continue
            
    print('\tfinished processing %s, took %.2f' % (fn, (time.time()-start)))
    return counter
        
        
if __name__ == '__main__':
    freeze_support()
    pool = Pool(4)
    result = pool.map(process, filenames)
    
    words = Counter()  # holds the count of all the words we see in tweets
    for c in result:
        words.update(c)
    
    with open(output_name, 'w', encoding='utf-8') as outfile:
        for word, count in words.items():
            outfile.write(word + '\t' + str(count) + '\n')
    