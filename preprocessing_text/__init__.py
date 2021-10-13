# std library
import re
import unicodedata

# 3rd party library
import pandas as pd
import numpy as np
import spacy
from spacy.lang.en.stop_words import STOP_WORDS as stop_words
from bs4 import BeautifulSoup
from textblob import TextBlob
from sklearn.feature_extraction.text import CountVectorizer

CONTRACTIONS = {
    "ain't": "am not",
    "aren't": "are not",
    "can't": "cannot",
    "can't've": "cannot have",
    "'cause": "because",
    "could've": "could have",
    "couldn't": "could not",
    "couldn't've": "could not have",
    "didn't": "did not",
    "doesn't": "does not",
    "don't": "do not",
    "hadn't": "had not",
    "hadn't've": "had not have",
    "hasn't": "has not",
    "haven't": "have not",
    "he'd": "he would",
    "he'd've": "he would have",
    "he'll": "he will",
    "he'll've": "he will have",
    "he's": "he is",
    "how'd": "how did",
    "how'd'y": "how do you",
    "how'll": "how will",
    "how's": "how does",
    "i'd": "i would",
    "i'd've": "i would have",
    "i'll": "i will",
    "i'll've": "i will have",
    "i'm": "i am",
    "i've": "i have",
    "isn't": "is not",
    "it'd": "it would",
    "it'd've": "it would have",
    "it'll": "it will",
    "it'll've": "it will have",
    "it's": "it is",
    "let's": "let us",
    "ma'am": "madam",
    "mayn't": "may not",
    "might've": "might have",
    "mightn't": "might not",
    "mightn't've": "might not have",
    "must've": "must have",
    "mustn't": "must not",
    "mustn't've": "must not have",
    "needn't": "need not",
    "needn't've": "need not have",
    "o'clock": "of the clock",
    "oughtn't": "ought not",
    "oughtn't've": "ought not have",
    "shan't": "shall not",
    "sha'n't": "shall not",
    "shan't've": "shall not have",
    "she'd": "she would",
    "she'd've": "she would have",
    "she'll": "she will",
    "she'll've": "she will have",
    "she's": "she is",
    "should've": "should have",
    "shouldn't": "should not",
    "shouldn't've": "should not have",
    "so've": "so have",
    "so's": "so is",
    "that'd": "that would",
    "that'd've": "that would have",
    "that's": "that is",
    "there'd": "there would",
    "there'd've": "there would have",
    "there's": "there is",
    "they'd": "they would",
    "they'd've": "they would have",
    "they'll": "they will",
    "they'll've": "they will have",
    "they're": "they are",
    "they've": "they have",
    "to've": "to have",
    "wasn't": "was not",
    " u ": " you ",
    " ur ": " your ",
    " n ": " and ",
    "won't": "would not",
    'dis': 'this',
    'bak': 'back',
    'brng': 'bring'}

nlp = spacy.load('en_core_web_sm')

get_word_counts = lambda x: len(str(x).split())
get_charcounts = lambda x: len(''.join(x.split()))
get_avg_wordlength = lambda x: get_charcounts(x) / get_word_counts(x)
get_stopwords_counts = lambda x: len([_ for _ in x.split() if _ in stop_words])
get_hashtag_counts = lambda x: len([_ for _ in x.split() if _.startswith('#')])
get_mention_counts = lambda x: len([_ for _ in x.split() if _.startswith('@')])
get_digit_counts = lambda x: len([_ for _ in x.split() if _.isdigit()])
get_uppercase_counts = lambda x: len([_ for _ in x.split() if _.isupper()])
get_emails = lambda x: len(re.findall(r'([a-z0-9+._-]+@[a-z0-9+._-]+\.[a-z0-9+_-]+\b)', x))


def count_exp(x):
    if isinstance(x, str):
        for key, value in CONTRACTIONS.items():
            if key in x:
                x = x.replace(key, value)
    return x


def get_emails(x):
    emails = re.findall(r'([a-z0-9+._-]+@[a-z0-9+._-]+\.[a-z0-9+_-]+\b)', x)
    return len(emails), emails


def get_urls(x):
    urls = re.findall(r'(http|https|ftp|ssh)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?', x)
    return len(urls), urls


def get_value_counts(df, col):
    text = ' '.join(df[col]).split()
    return pd.Series(text).value_counts()


def remove_common_words(x, freq, n=20):
    fn = freq[:n]
    return ' '.join([_ for _ in x.split() if _ not in fn])


def remove_rarewords(x, freq, n=20):
    fn = freq.tail(n)
    return ' '.join([_ for _ in x.split() if _ not in fn])


remove_emails = lambda x: re.sub(r'([a-z0-9+._-]+@[a-z0-9+._-]+\.[a-z0-9+_-]+)', "", x)
remove_urls = lambda x: re.sub(r'(http|https|ftp|ssh)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?','', x)
remove_rt = lambda x: re.sub(r'\b\rt\b','',x).strip()
remove_special_chars = lambda x: ' '.join(re.sub(r'[^\w]+',' ',x).split())
remove_html_tags = lambda x: BeautifulSoup(x, 'lxml').get_text().strip()
remove_accented_chars = lambda x: unicodedata.normalize('NFKD',x).encode('ascii', 'ignore').decode('utf-8', 'ignore')
remove_stopwords = lambda x: ' '.join([_ for _ in x.split() if _ not in stop_words])
make_base = lambda x: ' '.join([token.text if token.lemma_ == '-PRON-' or token.lemma_ == 'be' else token.lemma_ for token in nlp(str(x))])
spelling_correction = lambda x: TextBlob(x).correct()

def get_ngram(df, col, ngram_range):
	vectorizer = CountVectorizer(ngram_range=(ngram_range, ngram_range))
	vectorizer.fit_transform(df[col])
	ngram = vectorizer.vocabulary_
	ngram = sorted(ngram.items(), key = lambda x: x[1], reverse=True)
	return ngram
