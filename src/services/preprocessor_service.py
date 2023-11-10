import nltk
import re
import string

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet

# https://medium.com/analytics-vidhya/nlp-tutorial-for-text-classification-in-python-8f19cd17b49e

# Convert to lowercase, strip, and remove punctuations
def basic_preprocess(text):
    
    text = text.lower()
    
    text = text.strip()
    
    text = re.compile('<.*?>').sub('', text)
    
    text = re.compile('[%s]' % re.escape(string.punctuation)).sub(' ', text)
    
    text = re.sub('\s+', ' ', text)
    
    text = re.sub(r'\d', ' ', text)
    
    text = re.sub(r'\s+', ' ', text)
    return text

def stopword(string):
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(string)
    filtered_words = [word for word in words if word.lower() not in stop_words]
    return ' '.join(filtered_words)

def remove_smaller_words(words, word_len):
    filtered_words = [word for word in words if (len(word) > word_len)]
    return ' '.join(filtered_words)
    
def remove_non_english_words(string):
    english_words = set(word.lower() for word in nltk.corpus.words.words())
    words = word_tokenize(string)
    filtered_words = [word for word in words if (word.lower() in english_words and len(word) > 4)]
    return ' '.join(filtered_words)

def get_wordnet_pos(tag):
    if tag.startswith('J'):
        return wordnet.ADJ
    elif tag.startswith('V'):
        return wordnet.VERB
    elif tag.startswith('N'):
        return wordnet.NOUN
    elif tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN

def lemmatizer(string):
    word_pos_tags = nltk.pos_tag(word_tokenize(string))
    
    wl = WordNetLemmatizer()
    lemmatized_words = [wl.lemmatize(tag[0], get_wordnet_pos(tag[1])) for tag in word_pos_tags]
    return " ".join(lemmatized_words)

def preprocess(string):
    preprocessed_text = basic_preprocess(string)
    without_stopwords = stopword(preprocessed_text)
    without_small_and_stop_words = remove_smaller_words(without_stopwords, 3)
    lemmatized_text = lemmatizer(without_stopwords)
    return lemmatized_text

# text = "For writers, a random sentence can help them get their creative juices flowing. Since the topic of the sentence is completely unknown, it forces the writer to be creative when the sentence appears. There are a number of different ways a writer can use the random sentence for creativity. The most common way to use the sentence is to begin a story. Another option is to include it somewhere in the story. A much more difficult challenge is to use it to end a story. In any of these cases, it forces the writer to think creatively since they have no idea what sentence will appear from the tool."
# print(text)
# text = preprocess(text)
# print(text)