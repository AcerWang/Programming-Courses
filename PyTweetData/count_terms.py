from nltk.corpus import stopwords
import string
import operator 
import json
from collections import Counter
from collections import defaultdict

from text_process import TextProcessor

# If you run the script for the first time, uncomment the two code below
# import nltk
# nltk.download('stopwords')

fname = 'Blockchain.json'
with open(fname, 'r') as f:
    count_all = Counter()
    com = defaultdict(lambda : defaultdict(int))
    search_str = "eth"
    processor = TextProcessor()
    for line in f:
        if line.strip()=="":
            continue
        tweet = json.loads(line)
        # Create a list with all the terms
        punctuation = list(string.punctuation)
        stop = stopwords.words('english') + punctuation + ['RT','via','…','the','The']

        terms_only = [term.lower() for term in processor.preprocess(tweet['text']) if term not in stop and not term.startswith(('#','@'))]
        if search_str in terms_only:
            count_all.update(terms_only)
    print("Co-occurrence for %s:" % search_str)
    print(count_all.most_common(10))
    # Build co-occurrence matrix
    #     for i in range(len(terms_only)-1):            
    #         for j in range(i+1, len(terms_only)):
    #             w1, w2 = sorted([terms_only[i], terms_only[j]])              
    #             if w1 != w2:
    #                 com[w1][w2] += 1

    #     com_max = []
    #     # For each term, look for the most common co-occurrent terms
    # for t1 in com:
    #     t1_max_terms = sorted(com[t1].items(), key=operator.itemgetter(1), reverse=True)[:5]
    #     for t2, t2_count in t1_max_terms:
    #         com_max.append(((t1, t2), t2_count))
    # # Get the most frequent co-occurrences
    # terms_max = sorted(com_max, key=operator.itemgetter(1), reverse=True)
    # print(terms_max[:5])
    