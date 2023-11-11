
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.services.tiktok_recommendation_browser_session import TiktTokRecommendationBrowserSession

from src.database.models.post import Post
from src.twitter_apis.twitter_web_apis import tiktok_posts_recommendations_api, tiktok_posts_fasion_api
from src.utils.utils import save_dict_objs_to_csv

from src.services.mongodb_service import Mongodb_service
from src.configs.mongodb_config import scraped_posts_collection, scraped_posts_with_comments_collection, fasion_posts_collection

import asyncio
import json


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
    fetch_count = min(100, count)
    while(len(posts_from_api) < count and posts_response_data.get("hasMore", True)==True):
        posts_response_data = browser_session.make_request(tiktok_posts_fasion_api, {"count":fetch_count, "cursor":cursor})

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

def parse_api_reponse_and_get_main_attrinutes(posts_from_recommended_api, posts_from_fasion_api, browser_session):
    
    posts = []
    if posts_from_fasion_api is None:
        for post_from_recommended_api in posts_from_recommended_api:
            post_obj = Post(browser_session)
            post_obj = post_obj.mapper_recommended_api_resp_to_post(post_from_recommended_api)
            posts.append(post_obj)
    elif posts_from_recommended_api is None:
        for post_from_fasion_api in posts_from_fasion_api:
            post_obj = Post(browser_session)
            post_obj = post_obj.mapper_fasion_api_resp_to_post(post_from_fasion_api)
            posts.append(post_obj)
    
    return posts
       
def fetch_tiktok_posts_controller(posts_to_scrape, cursor):
    ms_token = "K0A_4yeeT2o4VZRofZzNhSGGjrstUFiE6FCrG9jtOWTKP_XtPFuCadkKj7yxbUNNNbNtPidJtBx62VwudNXJRHA_TEp5ZTxOZgi0jzy7Tzvv1WOjNR3CnhiPHDROJFcROQ5UT8WaRnPmb9cP"
    browser_session = TiktTokRecommendationBrowserSession(ms_token, True)
    
    # posts_from_api = fetch_tiktok_recommended_posts(10, browser_session)
    # posts = asyncio.run(parse_and_save_posts_from_api(posts_from_api, None, browser_session))
    
    posts_from_api_obj = fetch_tiktok_fasion_posts(posts_to_scrape, cursor, browser_session)
    posts_from_api = posts_from_api_obj["posts_from_api"]
    parsed_posts = parse_api_reponse_and_get_main_attrinutes(None, posts_from_api, browser_session)
    
    print("Fetched and parsed posts")
    parsed_posts_dic_objs = []
    for post in parsed_posts:
        post_dic = post.to_dict()
        post_dic["processed"] = False
        parsed_posts_dic_objs.append(post_dic)
    print("converted post objects to dic")
    
    try:
        mongodb_service = Mongodb_service(scraped_posts_collection)
        mongodb_service.save_many_to_mongodb(parsed_posts_dic_objs)
    except Exception as e:
        print(e)
        pass
        
    browser_session.close_session()
    
    return parsed_posts_dic_objs

async def fetch_comments_for_posts_controller(max_posts_to_process):
    
    mongodb_service_source = Mongodb_service(scraped_posts_collection)
    post_objs_mongo = mongodb_service_source.find_not_processed()
    post_objs_mongo[:max_posts_to_process]
        
    ms_token = "K0A_4yeeT2o4VZRofZzNhSGGjrstUFiE6FCrG9jtOWTKP_XtPFuCadkKj7yxbUNNNbNtPidJtBx62VwudNXJRHA_TEp5ZTxOZgi0jzy7Tzvv1WOjNR3CnhiPHDROJFcROQ5UT8WaRnPmb9cP"
    browser_session = TiktTokRecommendationBrowserSession(ms_token, False)
    
    post_objs = []
    mongo_ids = []
    
    for post_obj_mongo in post_objs_mongo:
        post_obj = Post(browser_session)
        print(post_obj_mongo)
        post_obj.mapper_dic_to_post(post_obj_mongo)
        post_objs.append(post_obj)
        mongo_ids.append(post_obj_mongo.get("_id"))
    
    print(len(post_objs))
    if(len(post_objs)>0):    
        browser_session.solve_captcha_for_other_sessions(post_objs[0].post_url)
        
        tasks = []
        for post_obj in post_objs:
            print(post_obj)
            task = asyncio.create_task(post_obj.scrape_comments_for_post())
            tasks.append(task)
        posts = await asyncio.gather(*tasks)
        
        browser_session.close_session()
        
        posts_dic_objs = []
        for post in posts:
            post_dic = post.to_dict()
            post_dic["processed"] = False
            posts_dic_objs.append(post_dic)
            
        mongodb_service = Mongodb_service(scraped_posts_with_comments_collection)
        mongodb_service.save_many_to_mongodb(posts_dic_objs)
        
        mongodb_service_source.update_processed_batch(mongo_ids)
        return posts_dic_objs
    else:
        return []       
    
def assign_relevance_scores_and_filter_fasion_posts(max_posts_to_process):
    
    mongodb_service_source = Mongodb_service(scraped_posts_with_comments_collection)
    post_objs_mongo = mongodb_service_source.find_not_processed()
    post_objs_mongo[:max_posts_to_process]
    
    post_objs = []
    mongo_ids= []
    for post_obj_mongo in post_objs_mongo:
        post_obj = Post(None)
        post_obj.mapper_dic_to_post(post_obj_mongo)
        post_objs.append(post_obj)
        mongo_ids.append(post_obj_mongo.get("_id"))
        
    posts_with_scores = []
    for post_obj in post_objs:
        post_with_scores = post_obj.calculate_and_assign_relavance_score_post()
        posts_with_scores.append(post_with_scores)
    
    fashion_posts = [post_with_scores for post_with_scores in posts_with_scores if post_with_scores.is_fasion_post]
    
    fashion_post_dic_objs = []
    for fashion_post in fashion_posts:
        fashion_post_dic = fashion_post.to_dict()
        fashion_post_dic_objs.append(fashion_post_dic)
    
    mongodb_service = Mongodb_service(fasion_posts_collection)
    mongodb_service.save_many_to_mongodb(fashion_post_dic_objs)
    
    # save_dict_objs_to_csv(fashion_post_dic_objs, "fasion_posts_with_relevance_scores.csv")
    mongodb_service_source.update_processed_batch(mongo_ids)
    
    return fashion_post_dic_objs
 
  
if __name__ == "__main__":
    # fetch_tiktok_posts_controller(300, 0)
    
    asyncio.run(fetch_comments_for_posts_controller(1))
    
    # assign_relevance_scores_and_filter_fasion_posts()
    
    
    pass
