import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from src.database.models.author import Author
from src.database.models.music import Music
from src.database.models.hashtags import Hashtags
from src.database.models.comment import Comment

from src.services.tiktok_recommendation_browser_session import TiktTokRecommendationBrowserSession

from src.services.mongodb_service import Mongodb_service
from src.configs.mongodb_config import fasion_posts_collection

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class Post:
    def __init__(self, post_item, browser_session):  
        self.browser_session = browser_session
              
        self.author = Author(post_item.get("author", {}), post_item.get("authorStats", {}))
        self.hashtags = Hashtags(post_item.get("challenges", []))
        self.music = Music(post_item.get("music", {}))
        
        self.comments = []
        self.video_id = post_item.get("video", []).get("id")
    
    def to_dict(self):
        # Convert the Post object to a dictionary
        post_dict = {
            "author": self.author.to_dict(),  # You may need to implement a to_dict method for Author
            "hashtags": self.hashtags.to_dict(),  # You may need to implement a to_dict method for Hashtags
            "music": self.music.to_dict(),  # You may need to implement a to_dict method for Music
            "comments": [comment.to_dict() for comment in self.comments],  # Convert comments to a list of dictionaries
            "video_id": self.video_id,
        }
        return post_dict
    
    def save_to_mongodb(self):
        
        mongodb_service = Mongodb_service(fasion_posts_collection)
        
        try:
            post_dict = self.to_dict()  # Convert the Post object to a dictionary
            if post_dict:
                mongodb_service.save_to_mongodb(post_dict)  # Save the dictionary to MongoDB
            else:
                raise Exception("No content to save")
        except Exception as e:
            print(e)
            raise Exception("Error saving content to MongoDB")
        
    async def fetchPostWithComments(self):
        
        # author_unique_id = self.author.unique_id
        # print(f"fetching commnets for https://www.tiktok.com/@{author_unique_id}/video/{self.video_id}")
        # self.browser_session.browser.switch_to.new_window('tab')
        # # self.browser_session.browser.switch_to.window(self.browser_session.browser.window_handles[-1])
        # self.browser_session.browser.get(f"https://www.tiktok.com/@{author_unique_id}/video/{self.video_id}")
    
        # self.browser_session.solve_captcha()
        # self.browser_session.close_signup_box()
        
        # comment_divs = self.browser_session.browser.find_elements(By.CSS_SELECTOR, '.tiktok-1mf23fd-DivContentContainer')
        # for comment_div in comment_divs:
        #     comment_text = comment_div.find_element(By.TAG_NAME, 'p').text
            
        #     comment_author = comment_div.find_element(By.CLASS_NAME, 'tiktok-fx1avz-StyledLink-StyledUserLinkName')
        #     comment_author_profile = comment_author.get_attribute('href')
        #     comment_author_id = comment_author.text
            
        #     print(Comment(comment_text, comment_author_profile, comment_author_id))
        #     self.comments.append(Comment(comment_text, comment_author_profile, comment_author_id))
                   
        # self.browser_session.browser.close()
        
        # https://www.tiktok.com/@martins_ji/video/7287589378447150342
        # api_url = "https://www.tiktok.com/api/comment/list/"
        # comments_response_data = self.browser_session.browser.make_request(api_url, {
        #         "aweme_id": self.video_id,
        #         "count": 20,
        #         "cursor": 0,
        #     })
        
        return self


