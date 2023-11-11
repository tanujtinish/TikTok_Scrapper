import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.services.text_classifier_service import TextClassifierService

import datetime
import csv

def calculate_statistical_relevance_score(post_obj):
    statistical_relevance_score = (post_obj.stats.comment_count + post_obj.stats.digg_count + post_obj.stats.play_count + post_obj.stats.share_count)
    
    date_posted = datetime.datetime.fromtimestamp(int(post_obj.date_posted))
    date_collected = post_obj.date_collected
    time_difference = date_collected - date_posted

    days_since_posted = time_difference.days
    
    statistical_relevance_score = statistical_relevance_score/days_since_posted
    post_obj.days_since_posted = days_since_posted

    return statistical_relevance_score


def calculate_relevance_score_using_processed_dataset(text):
    total_freq = 0

    fasion_word_freq = {}
    for word_list_csv in ["src/controllers/preprocessed_fasion_instagram_dataset/unique_brands.csv", "src/controllers/preprocessed_fasion_instagram_dataset/unique_categories.csv", "src/controllers/preprocessed_fasion_instagram_dataset/unique_hashtags.csv", "src/controllers/preprocessed_fasion_instagram_dataset/topic_words.csv"]:
        with open(word_list_csv, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                fasion_word = row[0].strip()
                fasion_word_freq[fasion_word] = 0

    words = text.split()
    for word in words:
        word = word.strip()
        if word in fasion_word_freq:
            fasion_word_freq[word] += 1

    # Calculate the total frequency
    total_freq = sum(fasion_word_freq.values())

    return total_freq

def calculate_relevance_score_fasion_labels(post_text_corpus):
    labels = ["fasion"]
    classifier_service = TextClassifierService()
    fasion_classification_result = classifier_service.classify_text(post_text_corpus, labels)
    fasion_classification_scores = fasion_classification_result.get("scores",{})
    
    
    post_relevance_score_fasion_labels = 0
    for score in fasion_classification_scores:
        post_relevance_score_fasion_labels = max(post_relevance_score_fasion_labels, score)
    
    return post_relevance_score_fasion_labels

def calculate_relavance_scores_for_a_post(post_obj):
    
    is_fasion_post = False
    
    post_obj.set_post_corpus()
    relevance_score_using_processed_dataset = calculate_relevance_score_using_processed_dataset(post_obj.post_text_corpus )
    if relevance_score_using_processed_dataset > 1:
        is_fasion_post = True
    
    post_relevance_score_fasion_labels = calculate_relevance_score_fasion_labels(post_obj.post_text_corpus )
    if post_relevance_score_fasion_labels > 0.5:
        is_fasion_post = True
    
    post_statistical_relevance_score = calculate_statistical_relevance_score(post_obj)
    # post_statistical_relevance_score = 0
    
    return {"relevance_score_using_processed_dataset":relevance_score_using_processed_dataset, "post_relevance_score_fasion_labels":post_relevance_score_fasion_labels, "post_statistical_relevance_score":post_statistical_relevance_score, "is_fasion_post":is_fasion_post}