import json
import re

# We define a class used to process tweets text as specific format
class TextProcessor:

    def __init__(self):
        # For emotion pattern
        self.emoticons_str = r"""
            (?:
                [:=;] # Eyes
                [oO\-]? # Nose (optional)
                [D\)\]\(\]/\\OpP] # Mouth
            )"""
        # self.emoji_str = u'[\U00010000-\U0010ffff]'
        # emoji_pattern = re.compile(
        #     u"(\ud83d[\ude00-\ude4f])|"  # emoticons
        #     u"(\ud83c[\udf00-\uffff])|"  # symbols & pictographs (1 of 2)
        #     u"(\ud83d[\u0000-\uddff])|"  # symbols & pictographs (2 of 2)
        #     u"(\ud83d[\ude80-\udeff])|"  # transport & map symbols
        #     u"(\ud83c[\udde0-\uddff])"   # flags (iOS)
        #     "+", flags=re.UNICODE)

        # For emotion, tags and others patterns
        self.regex_str = [
            self.emoticons_str,
            r'<[^>]+>', # HTML tags
            r'(?:@[\w_]+)', # @-mentions
            r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
            r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
        
            r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
            r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
            r'(?:[\w_]+)', # other words
            r'(?:\S)' # anything else
        ]
        
        self.tokens_re = re.compile(r'('+'|'.join(self.regex_str)+')', re.VERBOSE | re.IGNORECASE)
        self.emoticon_re = re.compile(r'^'+self.emoticons_str+'$', re.VERBOSE | re.IGNORECASE)

    # Match all kinds of patterns
    def tokenize(self,s):
        return self.tokens_re.findall(s)

    # Process text and return a list of splited parts.
    def preprocess(self,s , lowercase=False):
        tokens = self.tokenize(s)
        if lowercase:
            tokens = [token if self.emoticon_re.search(token) else token.lower() for token in tokens]
        return tokens

if __name__=='__main__':
    # Open file created before, each line contains data in json format.
    with open('./src/python.json', 'r') as f:
        for line in f:
            if line.strip() == "":
                continue
            
            # Load the json str, convert into a map
            tweet = json.loads(line)
            
            processor = TextProcessor()
            
            # Process tweets text information
            tokens = processor.preprocess(tweet['text'])
            print(tokens)