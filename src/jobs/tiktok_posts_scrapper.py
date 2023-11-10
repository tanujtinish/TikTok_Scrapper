
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.services.tiktok_recommendation_browser_session import TiktTokRecommendationBrowserSession

from src.database.models.post import Post
from src.twitter_apis.twitter_web_apis import tiktok_posts_recommendations_api, tiktok_posts_fasion_api

import asyncio


def fetch_tiktok_recommended_posts(count, browser_session):
    posts_from_api = []

    posts_response_data = {}
    while(len(posts_from_api) < count and posts_response_data.get("hasMore", True)==True):
        posts_response_data = browser_session.make_request(tiktok_posts_recommendations_api, {"count":count})

        if "itemList" in posts_response_data:
            posts_from_api.extend(posts_response_data["itemList"])
        else:
            pass

    if(len(posts_from_api) > 0):
        return posts_from_api
    else:
        return []

def fetch_tiktok_fasion_posts(count, cursor, browser_session):
    posts_from_api = []

    posts_response_data = {}
    while(len(posts_from_api) < count and posts_response_data.get("hasMore", True)==True):
        posts_response_data = browser_session.make_request(tiktok_posts_fasion_api, {"count":count, "cursor":cursor})

        if "items" in posts_response_data["videoList"]:
            posts_from_api.extend(posts_response_data["videoList"]["items"])
        else:
            pass

        posts_response_data = posts_response_data["videoList"]
        cursor = posts_response_data["cursor"]

    if(len(posts_from_api) > 0):
        return {"posts_from_api":posts_from_api, "cursor":cursor, "has_next":posts_response_data.get("hasMore")}
    else:
        return {"posts_from_api":[], "cursor":0, "has_next":False}

async def parse_and_save_post_from_api(post_from_recommended_api, post_from_fasion_api, fetch_comments, browser_session):
    
    post_obj = Post(post_from_recommended_api, post_from_fasion_api, browser_session)
    post_obj = post_obj.preprocess_and_fetch_main_attributes()
    
    if fetch_comments:
        post_obj = await post_obj.scrape_comments_for_post()
    else:
        pass
        
    return post_obj

async def parse_and_get_fasion_filtered_posts_from_api(posts_from_recommended_api, posts_from_fasion_api, fetch_comments, browser_session):
    
    if posts_from_fasion_api is None:
        post_obj = Post(posts_from_recommended_api[0], None, browser_session)
        post_obj = post_obj.preprocess_and_fetch_main_attributes()
        url = f"https://www.tiktok.com/@{post_obj.author.unique_id}/video/{post_obj.video_id}"
        browser_session.solve_captcha_for_other_sessions(url)
            
        tasks = []
        for post_from_recommended_api in posts_from_recommended_api:
            task = asyncio.create_task(parse_and_save_post_from_api(post_from_recommended_api, None, fetch_comments, browser_session))
            tasks.append(task)
        posts = await asyncio.gather(*tasks)
        
        for post in posts:
            post = post.calculate_and_assign_relavance_score_post()
            
    elif posts_from_recommended_api is None:
        post_obj = Post(None, posts_from_fasion_api[0], browser_session)
        post_obj = post_obj.preprocess_and_fetch_main_attributes()
        url = f"https://www.tiktok.com/@{post_obj.author.unique_id}/video/{post_obj.video_id}"
        browser_session.solve_captcha_for_other_sessions(url)
            
        tasks = []
        for post_from_fasion_api in posts_from_fasion_api:
            task = asyncio.create_task(parse_and_save_post_from_api(None, post_from_fasion_api, fetch_comments, browser_session))
            tasks.append(task)
        posts = await asyncio.gather(*tasks)
        
        for post in posts:
            post = post.calculate_and_assign_relavance_score_post()
    
    
    fashion_posts = [post for post in posts if post.is_fasion_post]
    return fashion_posts


def save_posts_to_database():
    for fashion_post in fashion_posts:
        print(fashion_post)
        fashion_post.save_to_mongodb()
        
def fetch_tiktok_fasion_posts_job(posts_to_scrape, fasion_posts_needed, fetch_comments):
    ms_token = "K0A_4yeeT2o4VZRofZzNhSGGjrstUFiE6FCrG9jtOWTKP_XtPFuCadkKj7yxbUNNNbNtPidJtBx62VwudNXJRHA_TEp5ZTxOZgi0jzy7Tzvv1WOjNR3CnhiPHDROJFcROQ5UT8WaRnPmb9cP"
    browser_session = TiktTokRecommendationBrowserSession(ms_token)
    
    fashion_posts = []
    fetched_fasion_posts_count = 0
    cursor = 0
    has_next = True
    if fasion_posts_needed==-1:
        posts_from_api_obj = fetch_tiktok_fasion_posts(posts_to_scrape, cursor, browser_session)
        
        posts_from_api = posts_from_api_obj["posts_from_api"]
        
        fashion_posts_fetched = asyncio.run(parse_and_get_fasion_filtered_posts_from_api(None, posts_from_api, fetch_comments, browser_session))
        
        fetched_fasion_posts_count = fetched_fasion_posts_count + len(fashion_posts_fetched)
        fashion_posts.extend(fashion_posts_fetched)
        
        # posts_from_api = fetch_tiktok_recommended_posts(10, browser_session)
        # posts = asyncio.run(parse_and_save_posts_from_api(posts_from_api, None, browser_session))
    else:
        while fetched_fasion_posts_count < fasion_posts_needed and has_next:
            posts_from_api_obj = fetch_tiktok_fasion_posts(fasion_posts_needed - fetched_fasion_posts_count, cursor, browser_session)
            
            posts_from_api = posts_from_api_obj["posts_from_api"]
            cursor = posts_from_api_obj["cursor"]
            has_next = posts_from_api_obj["has_next"]
            
            fashion_posts_fetched = asyncio.run(parse_and_get_fasion_filtered_posts_from_api(None, posts_from_api, fetch_comments, browser_session))
            
            fetched_fasion_posts_count = fetched_fasion_posts_count + len(fashion_posts_fetched)
            fashion_posts.extend(fashion_posts_fetched)
        
            # posts_from_api = fetch_tiktok_recommended_posts(10, browser_session)
            # posts = asyncio.run(parse_and_save_posts_from_api(posts_from_api, None, browser_session))

    browser_session.close_session()
    
    save_posts_to_database(fashion_posts)
    
    return fashion_posts

if __name__ == "__main__":
    fashion_posts =fetch_tiktok_fasion_posts_job(2, True)
