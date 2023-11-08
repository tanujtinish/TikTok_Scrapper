
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

class Comment:
    def __init__(self, comment_text, comment_author_profile, comment_author_id):
        
        self.comment = comment_text
        self.author = {"comment_author_profile":comment_author_profile, "comment_author_id":comment_author_id}
    
    
    