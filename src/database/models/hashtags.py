class Hashtags:
    def __init__(self, hashtags_data):
        self.titles = [hashtag.get("title", "") for hashtag in hashtags_data]
