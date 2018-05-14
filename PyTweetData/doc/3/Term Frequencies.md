# Term Frequencies

## 1. Introduction

After collecting data and pre-processing some text, we are ready for some basic analysis. In this part, we'll discuss the analysis of term frequencies to extract meaningful terms from our tweets.

## 2. Implementation

### *Step One*: Counting Terms

Assuming we have collected a list of tweets (see Part 1 of the course), the first exploratory analysis that we can perform is a simple word count. In this way, we can observe what are the terms most commonly used in the data set. In this example, I'll use the set of my tweets, so the most frequent words should correspond to the topics I discuss (not necessarily, but bear with be for a couple of paragraphs).

We can use a custom tokeniser to split the tweets into a list of terms. The following code uses the `preprocess()` function described (in Part 2 of the course), in order to capture Twitter-specific aspects of the text, such as #hashtags, @-mentions, emoticons and URLs. In order to keep track of the frequencies while we are processing the tweets, we can use `collections.Counter()` which internally is a dictionary (term: count) with some useful methods like `most_common()` , len(counter) will return number of elements(count once for the same element, that means the counter object seems like a `set` in some way):

```
import operator 
import json
from collections import Counter

from text_process import TextProcessor

fname = 'python.json'
with open(fname, 'r') as f:
    count_all = Counter()
    processor = TextProcessor()
    for line in f:
        if line.strip()=="":
            continue
        tweet = json.loads(line)
        # Create a list with all the terms
        terms_all = [term for term in processor.preprocess(tweet['text'])]
        # Update the counter
        count_all.update(terms_all)
    # Total number of terms
    print("There are",len(count_all),"terms.")
    # Print the first 10 most frequent words
    print(count_all.most_common(10))
```

The above code will produce some unimpressive results:

```
There are 501 terms.
[(':', 38), ('.', 36), ('…', 28), ('#Python', 27), ('RT', 24), ('#python', 22), ('for', 20), ('-', 18), ('Python', 16), ('the', 15)] 7)]
```

### *Step Two*: Removing stop-words

In every language, some words are particularly common. While their use in the language is crucial, they don't usually convey a particular meaning, especially if taken out of context. This is the case of articles, conjunctions, some adverbs, etc. which are commonly called *stop-words*. In the example above, we can see three common stop-words – *to*, *and* and *on*. Stop-word removal is one important step that should be considered during the pre-processing stages. One can build a custom list of stop-words, or use available lists (e.g. NLTK provides a simple list for English stop-words).

Given the nature of our data and our tokenization, we should also be careful with all the punctuation marks and with terms like *RT* (used for re-tweets) and *via* (used to mention the original author of an article or a re-tweet), which are not in the default stop-word list.

We can now substitute the variable `terms_all` with `terms_stop` in the first example with something like:

```
from nltk.corpus import stopwords
import string

# If you use this method and run the script for the first time,
# uncomment the two code below
# import nltk
# nltk.download('stopwords')

punctuation = list(string.punctuation)
stop = stopwords.words('english') + punctuation + ['rt','RT','via','…']
terms_stop = [term for term in processor.preprocess(tweet['text']) if term not in stop]
```

After counting, sorting the terms and printing the top 10, this is the result of my dataset:

```
There are 446 terms.
[('#Python', 27), ('#python', 22), ('Python', 16), ('☞', 13), ('Build', 6), ('Ultimate', 5), ('Developer', 5), ('Course', 5), ('Real', 5), ('Applications', 5)]
```

As you see, the result is case sensitive, and we did not filter the emoji emoticons, but the result is much better than before.

### *Step Three*: More term filters

Besides stop-word removal, we can further customise the list of terms/tokens we are interested in. Here you have some examples that you can embed in the first fragment of code:

```
# Count hashtags only, use `terms_hash` replace the one before 
terms_hash = [term for term in processor.preprocess(tweet['text']) 
              if term not in stop and term.startswith('#')]
# Count terms only (no hashtags, no mentions), use `terms_only` replace the one before
terms_only = [term for term in processor.preprocess(tweet['text']) 
              if term not in stop and not term.startswith(('#', '@'))] 
              # mind the ((double brackets))
              # startswith() takes a tuple (not a list)
```

After counting and sorting, these are most commonly used hashtags:

```
There are 63 hashtags.
[('#Python', 27), ('#python', 22), ('#Programming', 5), ('#Jupyter', 4), ('#django', 3), ('#hacking', 3), ('#Java', 3), ('#datascience', 3), ('#ArcGIS', 3), ('#flask', 2)]
```

and these are most commonly used terms:

```
There are 348 common terms.
[('Python', 16), ('☞', 13), ('Build', 6), ('Ultimate', 5), ('Developer', 5), ('Course', 5), ('Real', 5), ('Applications', 5), ('If', 4), ('looking', 4)]
```

While the other frequent terms represent a clear topic, more often than not simple term frequencies don't give us a deep explanation of what the text is about. To put things in context, let's consider sequences of two terms (a.k.a. *bigrams*).

```
from nltk import bigrams 

terms_bigram = bigrams(count_all) 
for item in terms_bigram:
    print(item)
```

The `bigrams()` function from NLTK will take a list of tokens and produce a list of tuples using adjacent tokens. Notice that we could use `terms_all` to compute the bigrams, but we would probably end up with a lot of garbage. In case we decide to analyse longer *n-grams* (sequences of *n* tokens), it could make sense to keep the stop-words, just in case we want to capture phrases like “to be or not to be”.

So after counting and sorting the bigrams, the result seems like:

```
('Data', 'Analysis')
('Analysis', 'Python')
('Python', 'amp')
('amp', 'Pandas')
('Pandas', '☞')
('☞', 'https://t.co/qSvFqF6JcE')
('https://t.co/qSvFqF6JcE', '#django')
('#django', '#python')
('#python', 'https://t.co/TQhF2I5ZwY')
('https://t.co/TQhF2I5ZwY', 'Why')
('Why', '#Jupyter')
('#Jupyter', 'Notebooks')
...
...
```

So apparently, I use the streaming API to get some data and make this case to show something interesting to you.

## 3. Summary

This part has built on top of the previous ones to discuss some basis for extracting interesting terms from a data set of tweets, by using simple term frequencies, stop-word removal and n-grams. While these approaches are extremely simple to implement, they are quite useful to have a bird's eye view on the data. We have used some components of NLTK, so we don't have to re-invent the wheel.