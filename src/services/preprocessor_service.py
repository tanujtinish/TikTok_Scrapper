import nltk
import re
import string
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')

# https://medium.com/analytics-vidhya/nlp-tutorial-for-text-classification-in-python-8f19cd17b49e

# Convert to lowercase, strip, and remove punctuations
def basic_preprocess(text):
    # Convert to lowercase
    text = text.lower()
    # Strip leading and trailing whitespaces
    text = text.strip()
    # Remove HTML tags
    text = re.compile('<.*?>').sub('', text)
    # Remove punctuation
    text = re.compile('[%s]' % re.escape(string.punctuation)).sub(' ', text)
    # Remove multiple spaces
    text = re.sub('\s+', ' ', text)
    # Remove digits
    text = re.sub(r'\d', ' ', text)
    # Remove extra whitespaces
    text = re.sub(r'\s+', ' ', text)
    return text

# STOPWORD REMOVAL
def stopword(string):
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(string)
    filtered_words = [word for word in words if word.lower() not in stop_words]
    return ' '.join(filtered_words)

# LEMMATIZATION
# Initialize the lemmatizer
wl = WordNetLemmatizer()

# This is a helper function to map NTLK position tags
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

# Tokenize the sentence
def lemmatizer(string):
    word_pos_tags = nltk.pos_tag(word_tokenize(string)) # Get position tags
    lemmatized_words = [wl.lemmatize(tag[0], get_wordnet_pos(tag[1])) for tag in word_pos_tags] # Map the position tag and lemmatize the word/token
    return " ".join(lemmatized_words)

# Final preprocessing combining all steps
def preprocess(string):
    preprocessed_text = basic_preprocess(string)
    without_stopwords = stopword(preprocessed_text)
    lemmatized_text = lemmatizer(without_stopwords)
    return lemmatized_text
