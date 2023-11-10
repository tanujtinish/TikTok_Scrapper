import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from datetime import datetime
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from src.database.models.author import Author
from src.database.models.music import Music
from src.database.models.hashtag import Hashtag
from src.database.models.comment import Comment
from src.database.models.stats import Stats

from src.services.tiktok_recommendation_browser_session import TiktTokRecommendationBrowserSession

from src.services.entity_linker_service import EntityLinkingService
from src.services.preprocessor_service import preprocess
from src.services.text_classifier_service import TextClassifierService

from src.services.mongodb_service import Mongodb_service
from src.configs.mongodb_config import fasion_posts_collection

class Post:
    def __init__(self, post_item_from_recommended_api, post_item_from_fasion_api, browser_session):  
        self.browser_session = browser_session
        self.post_item_from_recommended_api = post_item_from_recommended_api
        self.post_item_from_fasion_api = post_item_from_fasion_api
        
    
    def preprocess_and_fetch_main_attributes(self):
        
        if self.post_item_from_recommended_api is not None:
            post_item_from_recommended_api = self.post_item_from_recommended_api
            
            author_resp = post_item_from_recommended_api.get("author", {})
            self.author = Author(author_resp.get("id",""), author_resp.get("nickname",""), author_resp.get("uniqueId",""), author_resp.get("verified","") )
            self.hashtags = [Hashtag(hashtag['title'],hashtag['desc']) for hashtag in post_item_from_recommended_api.get("challenges", [])]
            
            music_resp = post_item_from_recommended_api.get("music", {})
            self.music = Music(music_resp.get("title",""),music_resp.get("authorName",""),music_resp.get("album",""))
            
            stats_resp = post_item_from_recommended_api.get("stats", {})
            self.stats = Stats(stats_resp.get("diggCount",0), stats_resp.get("playCount",0), stats_resp.get("shareCount",0), stats_resp.get("commentCount",0))
            
            self.caption = preprocess(post_item_from_recommended_api.get("desc", {}))
            self.date_posted = post_item_from_recommended_api.get("createTime", {})
            self.date_collected = datetime.now()
            
            self.comments = []
            self.video_id = post_item_from_recommended_api.get("video", []).get("id")
            self.post_url = f"https://www.tiktok.com/@{self.author.unique_id}/video/{self.video_id}"
        elif self.post_item_from_fasion_api is not None:
            post_item_from_fasion_api = self.post_item_from_fasion_api
            self.author = Author(post_item_from_fasion_api.get("authorId",""), post_item_from_fasion_api.get("authorNickname",""), post_item_from_fasion_api.get("authorUniqueId",""), post_item_from_fasion_api.get("authorVerified",""))
            self.hashtags = [Hashtag(hashtag,"") for hashtag in post_item_from_fasion_api.get("hashtagList", [])]
            
            self.music = Music(post_item_from_fasion_api.get("musicTitle",""),post_item_from_fasion_api.get("musicAuthorName",""),post_item_from_fasion_api.get("musicAlbum",""))
            self.stats = Stats(post_item_from_fasion_api.get("diggCount", 0), post_item_from_fasion_api.get("playCount", 0), post_item_from_fasion_api.get("shareCount", 0), post_item_from_fasion_api.get("playCount", 0))
            
            self.caption = preprocess(post_item_from_fasion_api.get("desc", {}))
            self.date_posted = post_item_from_fasion_api.get("createTime", {})
            self.date_collected = datetime.now()
            
            self.comments = []
            self.video_id = post_item_from_fasion_api.get("id", [])
            self.post_url = f"https://www.tiktok.com/@{self.author.unique_id}/video/{self.video_id}"
            
            pass
        
        return self
        
    def to_dict(self):
        # Convert the Post object to a dictionary
        post_dict = {
            "video_id": self.video_id,
            "post_url": self.post_url,
            "caption": self.caption,
            
            "author": self.author.to_dict(), 
            
            "music": self.music.to_dict(),  
            "hashtags": [hashtag.to_dict() for hashtag in self.hashtags],
            "comments": [comment.to_dict() for comment in self.comments],
            
            "stats": self.stats.to_dict(),
            
            "date_posted": self.date_posted,
            "date_collected": self.date_collected,
            
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
            raise Exception("Error saving content to MongoDB")
    
    
    def calculate_and_assign_relavance_score_post(self):
        
        entity_linking_service = EntityLinkingService()
        post_entities = [hashtag.title for hashtag in self.hashtags]
        
        #calculating post_text_corpus_fasion_relevance_score
        post_text_corpus = self.caption
        for hashtag in self.hashtags:
            if hashtag.desc!="":
                post_text_corpus = post_text_corpus + " " + hashtag.desc + " " + hashtag.title
            else:
                post_text_corpus = post_text_corpus + " " + hashtag.title
        for comment in self.comments:
            post_text_corpus = post_text_corpus + " " + comment.comment
            
        linked_entities_in_post_text_corpus = entity_linking_service.link_entities(post_text_corpus)
        post_entities.extend(linked_entities_in_post_text_corpus)
        
        for entity in post_entities:
            post_text_corpus = post_text_corpus + entity
        
        
        labels = ["fasion"]
        classifier_service = TextClassifierService()
        fasion_classification_result = classifier_service.classify_text(post_text_corpus, labels)
        fasion_classification_scores = fasion_classification_result.get("scores")
        
        self.entities = post_entities
        self.post_text_corpus = post_text_corpus
        self.post_text_corpus_fasion_relevance_score = 0
        for score in fasion_classification_scores:
            self.post_text_corpus_fasion_relevance_score = max(self.post_text_corpus_fasion_relevance_score, score)
        
        if self.post_text_corpus_fasion_relevance_score > 0.5:
            self.is_fasion_post = True
        else:
            self.is_fasion_post = False
        
        self.post_relevance_score = (self.stats.comment_count + self.stats.digg_count + self.stats.play_count + self.stats.share_count)
        
        print(post_text_corpus)
        print(self.post_text_corpus_fasion_relevance_score)
        print(self.post_relevance_score)
        print(self.is_fasion_post)
        print("")
        
        return self
        
    async def scrape_comments_for_post(self):
        
        print(f"fetching commnets for {self.post_url}")
        self.browser_session.browser.switch_to.new_window('tab')
        # self.browser_session.browser.switch_to.window(self.browser_session.browser.window_handles[-1])
        self.browser_session.browser.get(self.post_url)
    
        self.browser_session.solve_captcha()
        self.browser_session.close_signup_box()
        
        comment_divs = self.browser_session.browser.find_elements(By.CSS_SELECTOR, '.tiktok-1mf23fd-DivContentContainer')
        for comment_div in comment_divs:
            comment_text = comment_div.find_element(By.TAG_NAME, 'p').text
            
            comment_author = comment_div.find_element(By.CLASS_NAME, 'tiktok-fx1avz-StyledLink-StyledUserLinkName')
            comment_author_profile = comment_author.get_attribute('href')
            comment_author_id = comment_author.text
            
            self.comments.append(Comment(comment_text, comment_author_profile, comment_author_id))
                           
        # https://www.tiktok.com/@martins_ji/video/7287589378447150342
        # api_url = "https://www.tiktok.com/api/comment/list/"
        # comments_response_data = self.browser_session.browser.make_request(api_url, {
        #         "aweme_id": self.video_id,
        #         "count": 20,
        #         "cursor": 0,
        #     })
        
        return self


