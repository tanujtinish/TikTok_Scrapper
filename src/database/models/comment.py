
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.services.preprocessor_service import preprocess

class Comment:
    def __init__(self, comment_text, comment_author_profile, comment_author_id):
        self.comment = preprocess(comment_text)
        self.author = {
            "comment_author_profile": comment_author_profile,
            "comment_author_id": comment_author_id
        }
    
    def to_dict(self):
        # Convert the Comment object to a dictionary
        comment_dict = {
            "comment": self.comment,
            "author": self.author
        }
        return comment_dict
    
    @staticmethod
    def from_dict( comment_dict):
        comment_text = comment_dict.get("comment","")
        comment_author_profile = comment_dict.get("author","").get("comment_author_profile","")
        comment_author_id = comment_dict.get("author","").get("comment_author_id","")
        
        comment= Comment(
            comment_text, comment_author_profile, comment_author_id
        )
        return comment
    
    
    