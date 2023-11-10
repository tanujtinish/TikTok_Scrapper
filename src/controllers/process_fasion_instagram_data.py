import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.services.preprocessor_service import preprocess, remove_non_english_words
from src.services.topic_modelling_service import TopicModelingService
from src.utils.utils import  word_frequency_in_list

import pandas as pd
import csv

def process_fasion_instagram_data(num_topics, words_per_topic):
    df = pd.read_csv('src/datasets/fashion_data_on_Instagram.csv')

    # Fetch unique values from the desired columns
    unique_brands = df['BrandName'].unique()
    unique_categories = df['BrandCategory'].unique()
    df['Hashtags'] = df['Hashtags'].str.split(', ')
    unique_hashtags = df['Hashtags'].explode().unique()

    # Convert them to lists if needed
    brand_list = unique_brands.tolist()
    category_list = unique_categories.tolist()
    hashtag_list = unique_hashtags.tolist()

    pd.Series(brand_list).to_csv('src/controllers/preprocessed_fasion_instagram_dataset/unique_brands.csv', index=False, header=['BrandName'])
    pd.Series(category_list).to_csv('src/controllers/preprocessed_fasion_instagram_dataset/unique_categories.csv', index=False, header=['BrandCategory'])
    pd.Series(hashtag_list).to_csv('src/controllers/preprocessed_fasion_instagram_dataset/unique_hashtags.csv', index=False, header=['Hashtags'])

    combined_caption =  df['Caption'].str.cat(sep=' ')
    preprocessed_combined_caption = preprocess(combined_caption)
    preprocessed_combined_caption = remove_non_english_words(preprocessed_combined_caption)

    # preprocessed_combined_caption = "i am tanuj live good sexy crazy life haha im coool ho r you"
    topic_modeling_service = TopicModelingService(num_topics)
    lda_model = topic_modeling_service.train_lda_model(preprocessed_combined_caption)

    # Print the topics
    topics_list = topic_modeling_service.get_topic_words(lda_model, words_per_topic)

    all_words = []
    for topic in topics_list:
        words = topic[1].split('+')
        
        for word in words:
            cleaned_word = word.split('"')[1]
            all_words.append(cleaned_word)

    with open('src/controllers/preprocessed_fasion_instagram_dataset/topic_words.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        all_words = set(all_words)
        
        word_frequency_in_list_map = word_frequency_in_list(all_words)
        
        for word, freq in word_frequency_in_list_map:
            writer.writerow([word])
