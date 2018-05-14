# Blockchain and Term Co-occurrences

## 1. Introduction

This part continues the tutorial on Twitter Data Mining, re-using what we discussed in the previous parts with some more realistic data. It also expands the analysis by introducing the concept of term co-occurrence.

## 2. Implementation

### *Step One*: The Application Domain

As the name suggests, six teams are involved in the competition: England, Ireland, Wales, Scotland, France and Italy. This means that we can expect the event to be tweeted in multiple languages (English, French, Italian, Welsh, Gaelic, possibly other languages as well), with English being the major language. Assuming the team names will be mentioned frequently, we could decide to look also for their nicknames, e.g. *Les Bleus* for France or *Azzurri* for Italy. During the last day of the competition, three matches are played sequentially. Three teams in particular had a shot for the title: England, Ireland and Wales. At the end, Ireland won the competition but everything was open until the very last minute.

### *Step Two*: Setting Up

I used the streaming API to download tweets containing the string `#blockchain` during the day. Obviously not all the tweets about the topic contained the hashtag, but this is a good baseline. The time frame for the download was from around **04:42 to 05:00** , **05:47 to 06:01** , **06:55 to 07:10** , **08:00 to 08:05** , **09:00 to 09:07** that is a time span about 5~15 minutes per time frame. At the end, more than **10,000 tweets** have been downloaded in JSON format, making for about **60Mb** of data. This should be small enough to quickly do some processing in memory, and at the same time big enough to observe something possibly interesting.

The textual content of the tweets has been pre-processed with *tokenisation and lowercasing* using the `preprocess()` function introduced in Part 2 of the course.

### *Step Three*: Interesting Terms and Hashtags

Following what we discussed in Part 3 (Term Frequencies), we want to observe the most common terms and hashtags used during day. If you have followed the discussion about creating different lists of tokens in order to capture terms without hashtags, hashtags only, removing stop-words, etc. you can play around with the different lists.

The top 10 most frequent terms in the data set:

```
Total terms:  5267
[('we', 337), ('join', 277), ('🔥', 196), ('token', 187), ('new', 181), ('ico', 175), ('us', 166), ('blockchain', 162), ('️', 141), ('tokens', 134)]
```

Interestingly, a new token we didn't account for, an Emoji symbol, it represent that the concept of blockchain is very hot all around the world, in fact it is.

This is the unsurprising list of top 10 most frequent hashtags (`terms_only` in Part 3) in the data set. The are several terms correspond to the topic who had a go for the title. 

```
Total hashtags:  1092
[('#blockchain', 1237), ('#ico', 329), ('#crypto', 310), ('#bitcoin', 286), ('#cryptocurrency', 230), ('#iot', 203), ('#ethereum', 171), ('#ai', 133), ('#tokensale', 106), ('#airdrop', 105)]
```

The frequencies also respect the popularity of each term. If we dig into the data, there will be more potential value to be discovered, and underlying relationships of trend.

### *Step Four*: Term co-occurrences

Sometimes we are interested in the terms that occur together. This is mainly because the *context* gives us a better insight about the meaning of a term, supporting applications such as word disambiguation or semantic similarity. We discussed the option of using *bigrams* in the previous part, but we want to extend the context of a term to the whole tweet.

We can refactor the code from the previous part in order to capture the **co-occurrences**. We build a co-occurrence matrix `com` such that `com[x][y]` contains the number of times the term `x`has been seen in the same tweet as the term `y`:

```
from collections import defaultdict
# remember to include the other import from the previous post
 
com = defaultdict(lambda : defaultdict(int))
 
# f is the file pointer to the JSON data set
for line in f: 
    tweet = json.loads(line)
    terms_only = [term for term in processor.preprocess(tweet['text']) 
                  if term not in stop and not term.startswith(('#', '@'))]
 
    # Build co-occurrence matrix
    for i in range(len(terms_only)-1):            
        for j in range(i+1, len(terms_only)):
            w1, w2 = sorted([terms_only[i], terms_only[j]])                
            if w1 != w2:
                com[w1][w2] += 1
```

While building the co-occurrence matrix, we don't want to count the same term pair twice, e.g. `com[A][B] == com[B][A]`, so the inner for loop starts from `i+1` in order to build a triangular matrix, while `sorted` will preserve the alphabetical order of the terms.

For each term, we then extract the 5 most frequent co-occurrent terms, creating a list of tuples in the form `((term1, term2), count)`:

```
com_max = []
# For each term, look for the most common co-occurrent terms
for t1 in com:
    t1_max_terms = sorted(com[t1].items(), key=operator.itemgetter(1), reverse=True)[:5]
    for t2, t2_count in t1_max_terms:
        com_max.append(((t1, t2), t2_count))
# Get the most frequent co-occurrences
terms_max = sorted(com_max, key=operator.itemgetter(1), reverse=True)
print(terms_max[:5])
```

The results (This may take you about 1~2 minutes to get the result, it depends on how big your data set is):

```
[(('⭐', '️'), 294), (('❄', '️'), 160), (('lot', 'we'), 156), (('getting', 'we'), 154), (('believe', 'we'), 154)]
```

This implementation is pretty straightforward, but depending on the data set and on the use of the matrix, one might want to look into tools like `scipy.sparse` for building a sparse matrix.

We could also look for a specific term and extract its most frequent co-occurrences. We simply need to modify the main loop including an extra counter, for example:

```
# pass a term as argument
search_word = "bitcoin"  # or btc
count_search = Counter()
for line in f:
    tweet = json.loads(line)
    terms_only = [term for term in preprocess(tweet['text']) 
                  if term not in stop 
                  and not term.startswith(('#', '@'))]
    if search_word in terms_only:
        count_search.update(terms_only)
print("Co-occurrence for %s:" % search_word)
print(count_search.most_common(20))
```

The count result for 'bitcoin':

```
Co-occurrence for bitcoin:
[('bitcoin', 83), ('03', 21), ('ethereum', 21), ('09', 17), ('2018', 17), ('₺', 16), ('cash', 11), ('02', 10), ('bch', 9), ('live', 9)]
```

The count result for 'eth':

```
Co-occurrence for eth:
[('eth', 84), ('hard', 46), ('cap', 46), ('next', 34), ('20', 24), ('000', 24), ('upcoming', 23), ('our', 23), ('🙂', 23), ('1', 19)]
```

## 3. Summary

This part has discussed a toy example of Text Mining on Twitter, using some realistic data taken during a day. Using what we have learnt in the previous episodes, we have downloaded some data using the streaming API, pre-processed the data in JSON format and extracted some interesting terms and hashtags from the tweets. We have also introduced the concept of term co-occurrence, shown how to build a co-occurrence matrix and discussed how to use it to find some interesting insight.