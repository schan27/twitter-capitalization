# usage: python process_google.py <google_dir>
#
# for each google n-gram file in <dir>, output a file in the same directory
# where each line has the following format:
#   word <tab> count
# only words which occurred more than 100 times from 2000 onward are considered

import os
import sys
import time
import pandas as pd

GOOGLE_DIR = sys.argv[1]

def csv_chunks(path, chunk_size):
    reader = pd.read_csv(path, 
        encoding='utf-8', 
        low_memory=False, 
        sep='\t', 
        header=None, 
        chunksize=chunk_size)
        
    for chunk in reader:
        yield chunk


# dataset downloaded from
# http://storage.googleapis.com/books/ngrams/books/datasetsv2.html
def process_google(dir_name):
    for entry in os.scandir(dir_name):
        fn = entry.name
        if not fn.startswith('google') or fn.endswith('.words'):
            continue
            
        start = time.time()
        
        chunks = []
        for chunk in csv_chunks(os.path.join(dir_name, fn), 100000):
            # word only contains alphabetical characters, and year is greater than
            # or equal to 2000
            chunk = chunk[(chunk[0].str.isalpha() == True) & (chunk[1] >= 2000)]        
            chunks.append(chunk)
        df = pd.concat(chunks)
        grouped = df.groupby([0])  # group by word
        
        rows = []
        for word, indices in grouped.indices.items():
            count = df.iloc[indices][2].sum()   # add up number of instances from all years
            if count >= 100: 
                rows.append(word + '\t' + str(count) + '\n')
                
        with open(os.path.join(dir_name, fn + '.words'), 'w', encoding='utf-8') as outfile:
            outfile.writelines(words)
            
        print('\tfinished processing %s, took %.2f' % (fn, (time.time()-start)))
        
    return True
    
    
process_google(GOOGLE_DIR)