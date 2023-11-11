import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.services.preprocessor_service import preprocess

class Hashtag:
    def __init__(self, title, desc):
        self.title = preprocess(title)
        self.desc = preprocess(desc)

    def to_dict(self):
        # Convert the Hashtags object to a dictionary
        hashtags_dict = {
            "title": self.title,
            "desc": self.desc,
        }
        return hashtags_dict
    
    @staticmethod
    def from_dict( hashtag_dict):
        title = hashtag_dict.get("title","")
        desc = hashtag_dict.get("desc","")
        
        hashtag= Hashtag(
            title, desc
        )
        return hashtag