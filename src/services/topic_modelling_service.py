from gensim import corpora, models
import gensim

class TopicModelingService:
    def __init__(self, num_topics=3):
        self.num_topics = num_topics

    def train_lda_model(self, data):
        # Create a dictionary and corpus for LDA
        
        tokenized_data = [word for word in data.split()]
        dictionary = corpora.Dictionary([tokenized_data])
        corpus = [dictionary.doc2bow(tokenized_data)]

        # Train the LDA model
        lda_model = gensim.models.LdaModel(
            corpus, num_topics=self.num_topics, id2word=dictionary, passes=15, random_state=42
        )

        return lda_model

    def get_topic_words(self, lda_model, words_per_topic):
        # Print the topics
        topic_words = lda_model.print_topics(num_words=words_per_topic)
        return topic_words
