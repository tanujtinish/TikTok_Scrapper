import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import csv

def word_frequency(sentence):
    words = sentence.split()
    word_freq_map = {}

    for word in words:
        if word in word_freq_map:
            word_freq_map[word] += 1
        else:
            word_freq_map[word] = 1

    sorted_word_freq_map = sorted(word_freq_map.items(), key=lambda x: x[1], reverse=True)
    return sorted_word_freq_map

def word_frequency_in_list(word_list):
    word_freq_map = {}

    for word in word_list:
        if word in word_freq_map:
            word_freq_map[word] += 1
        else:
            word_freq_map[word] = 1
            
    sorted_word_freq_map = sorted(word_freq_map.items(), key=lambda x: x[1], reverse=True)
    return sorted_word_freq_map


def save_dict_objs_to_csv(list_of_dicts, filename):
    with open("src/database/csv_data/"+filename, 'w', newline='') as csvfile:
        
        if len(list_of_dicts)==0:
            return
        
        fieldnames = list_of_dicts[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        
        for row in list_of_dicts:
            writer.writerow(row)