import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from datetime import datetime
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import csv
import json
import pandas as pd


from src.database.models.author import Author
from src.database.models.music import Music
from src.database.models.hashtag import Hashtag
from src.database.models.comment import Comment
from src.database.models.stats import Stats

from src.services.tiktok_recommendation_browser_session import TiktTokRecommendationBrowserSession
from src.services.entity_linker_service import EntityLinkingService
from src.services.relevance_score_service import calculate_relavance_scores_for_a_post

from src.services.preprocessor_service import preprocess

# from src.services.mongodb_service import Mongodb_service
from src.configs.mongodb_config import fasion_posts_collection

class Post:
    def __init__(self, browser_session):  
        self.browser_session = browser_session
        
        self.video_id=""
        self.post_url=""
        self.caption=""
        self.author = {}
        self.music = {}
        self.hashtags = []
        self.comments = []
        self.stats = {}
        self.date_posted = ""
        self.date_collected = ""
        self.days_since_posted = ""
        self.entities = []
        self.post_text_corpus=""
        self.relevance_score_using_processed_dataset =0
        self.post_relevance_score_fasion_labels=0
        self.post_statistical_relevance_score=0
        self.is_fasion_post=False
    
    def set_post_corpus(self):
        entity_linking_service = EntityLinkingService()
        post_entities = [hashtag.title for hashtag in self.hashtags]
        
        #calculating post_text_corpus_fasion_relevance_score
        post_text_corpus = str(self.caption)
        for hashtag in self.hashtags:
            if hashtag.desc!="":
                post_text_corpus = post_text_corpus + " " + str(hashtag.desc) + " " + str(hashtag.title)
            else:
                post_text_corpus = post_text_corpus + " " + str(hashtag.title)
        for comment in self.comments:
            post_text_corpus = post_text_corpus + " " + str(comment.comment)
            
        linked_entities_in_post_text_corpus = entity_linking_service.link_entities(post_text_corpus)
        post_entities.extend(linked_entities_in_post_text_corpus)
        
        for entity in post_entities:
            post_text_corpus = post_text_corpus + entity
        
        self.entities = post_entities
        self.post_text_corpus = post_text_corpus
        
        return self
    
    def mapper_recommended_api_resp_to_post(self,post_item_from_recommended_api ):
                
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
        self.video_id = post_item_from_recommended_api.get("video", []).get("id","")
        self.post_url = f"https://www.tiktok.com/@{self.author.unique_id}/video/{self.video_id}"
          
        return self
    
    def mapper_fasion_api_resp_to_post(self, post_item_from_fasion_api):
        
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
                
        return self
    
    def mapper_csv_row_to_post(self, row):
        author =json.loads(row['author'].replace("\'", "\""))
        hashtags = json.loads(row['hashtags'].replace("\'", "\""))
        comments = json.loads(row['comments'].replace("\'", "\""))
        music = json.loads(row['music'].replace("\'", "\""))
        stats = json.loads(row['stats'].replace("\'", "\""))
    
        self.video_id=row['video_id'],
        self.post_url=row['post_url'],
        self.caption=row['caption'],
        self.author= Author.from_dict(author)
        self.music=Music.from_dict(music),   
        self.hashtags=[Hashtag.from_dict(item) for item in hashtags],
        self.comments=[Comment.from_dict(item) for item in comments],
        self.stats=Stats.from_dict(stats),
        self.date_posted=row['date_posted'],
        self.date_collected=row['date_collected']
        
        return self
        
    
    @staticmethod
    def mapper_csv_to_posts(csv_filename, browser_session):
        posts = []
        
        with open(csv_filename, 'r', newline='') as csvfile:
            df = pd.read_csv(csv_filename)
            
            for _, row in df.iterrows():
                # Create a Post object from the dictionary
                post = Post(browser_session)
                post = post.mapper_csv_row_to_post(row)
                
                post.video_id=post.video_id[0]
                post.post_url=post.post_url[0]
                post.caption=post.caption[0]
                post.author=post.author
                post.music=post.music[0]
                post.hashtags=post.hashtags[0]
                post.comments=post.comments[0]
                post.stats=post.stats[0]
                post.date_posted=post.date_posted[0]
                post.date_collected=post.date_collected[0]
                
                posts.append(post)
    
        return posts
    
    def mapper_dic_to_post(self, post_dic_ob):
            
        self.video_id=post_dic_ob.get("video_id")
        self.post_url=post_dic_ob.get("post_url")
        self.caption=post_dic_ob.get("caption","")
        self.author= Author.from_dict(post_dic_ob.get("author",""))
        
        
        
        self.date_posted=post_dic_ob.get("date_posted")
        self.date_collected=post_dic_ob.get("date_collected")
        
        self.music=Music.from_dict(post_dic_ob.get("music","")),   
        self.music=self.music[0]
        
        self.stats=Stats.from_dict(post_dic_ob.get("stats",""))
        
        self.hashtags=[Hashtag.from_dict(item) for item in post_dic_ob.get("hashtags",[])],
        self.hashtags=self.hashtags[0]
        
        self.comments=[Comment.from_dict(item) for item in post_dic_ob.get("comments",[])],
        self.comments=self.comments[0]
        

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
            "days_since_posted": self.days_since_posted,
            
            "post_entities": self.entities,
            "post_text_corpus": self.post_text_corpus,
            
            "relevance_score_using_processed_dataset": self.relevance_score_using_processed_dataset,
            "post_relevance_score_fasion_labels": self.post_relevance_score_fasion_labels,
            "post_statistical_relevance_score": self.post_statistical_relevance_score,
            "is_fasion_post": self.is_fasion_post,
            
        }
        return post_dict
    
    def calculate_and_assign_relavance_score_post(self):
        
        relavance_scores_for_a_post = calculate_relavance_scores_for_a_post(self)
        self.relevance_score_using_processed_dataset = relavance_scores_for_a_post["relevance_score_using_processed_dataset"]
        self.post_relevance_score_fasion_labels = relavance_scores_for_a_post["post_relevance_score_fasion_labels"]
        self.post_statistical_relevance_score = relavance_scores_for_a_post["post_statistical_relevance_score"]
        self.is_fasion_post = relavance_scores_for_a_post["is_fasion_post"]
        
        return self
        
    async def scrape_comments_for_post(self):
        
        print(f"fetching commnets for {self.post_url}")
        self.browser_session.browser.switch_to.new_window('tab')
        # self.browser_session.browser.switch_to.window(self.browser_session.browser.window_handles[-1])
        self.browser_session.browser.get(self.post_url)
    
        self.browser_session.solve_captcha()
        self.browser_session.close_signup_box()
        
        comment_divs = self.browser_session.browser.find_elements(By.CSS_SELECTOR, '.tiktok-1mf23fd-DivContentContainer')
        print(len(comment_divs))
        print(comment_divs)
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


