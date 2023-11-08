class Hashtags:
    def __init__(self, hashtags_data):
        self.titles = [hashtag.get("title", "") for hashtag in hashtags_data]

    def to_dict(self):
        # Convert the Hashtags object to a dictionary
        hashtags_dict = {
            "titles": self.titles,
        }
        return hashtags_dict