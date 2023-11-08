import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from src.database.models.author import Author
from src.database.models.music import Music
from src.database.models.hashtags import Hashtags
from src.database.models.comment import Comment

from src.services.tiktok_recommendation_browser_session import TiktTokRecommendationBrowserSession

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import asyncio

class Post:
    def __init__(self, post_item, browser_session):        
        self.author = Author(post_item.get("author", {}), post_item.get("authorStats", {}))
        self.hashtags = Hashtags(post_item.get("challenges", []))
        self.music = Music(post_item.get("music", {}))
        
        self.comments = []
        self.video_id = post_item.get("video", []).get("id")
        self.browser_session = browser_session

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

class Posts:
    def __init__(self, browser_session):
        self.browser_session = browser_session
        self.posts = []
        
        self.posts_response_data = self.fetch_posts()
    
    def fetch_posts(self):
        # Make a request using the session
        api_url = "https://www.tiktok.com/api/recommend/item_list/"
        posts_response_data = self.browser_session.make_request(api_url, {"count":30})
        
        return posts_response_data
    
    async def parse_response(self):
        if "itemList" in self.posts_response_data:
            itemList = self.posts_response_data["itemList"]
        else:
            itemList = []
        
        
        if(len(itemList) > 0):
            post_obj = Post(itemList[0], self.browser_session)
            url = f"https://www.tiktok.com/@{post_obj.author.unique_id}/video/{post_obj.video_id}"
            # url = "https://google.com"
            self.browser_session.solve_captcha_for_other_sessions(url)
            
            tasks = []
            for item in itemList:
                post_obj = Post(item, self.browser_session)
                task = asyncio.create_task(post_obj.fetchPostWithComments())
                tasks.append(task)
            
            results = await asyncio.gather(*tasks)
            self.posts = results
        else:
            self.posts = []
        
        
    
   
