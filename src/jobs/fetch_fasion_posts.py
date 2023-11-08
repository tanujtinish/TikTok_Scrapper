
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.services.tiktok_recommendation_browser_session import TiktTokRecommendationBrowserSession

from src.database.models.post import Post

import asyncio


async def fetch_fasion_trending_posts(count):
    # Example usage:
    ms_token = "K0A_4yeeT2o4VZRofZzNhSGGjrstUFiE6FCrG9jtOWTKP_XtPFuCadkKj7yxbUNNNbNtPidJtBx62VwudNXJRHA_TEp5ZTxOZgi0jzy7Tzvv1WOjNR3CnhiPHDROJFcROQ5UT8WaRnPmb9cP"
    browser_session = TiktTokRecommendationBrowserSession(ms_token)

    # Make a request using the session
    api_url = "https://www.tiktok.com/api/recommend/item_list/"
    posts_response_data = browser_session.make_request(api_url, {"count":count})

    if "itemList" in posts_response_data:
        itemList = posts_response_data["itemList"]
    else:
        itemList = []


    if(len(itemList) > 0):
        post_obj = Post(itemList[0], browser_session)
        url = f"https://www.tiktok.com/@{post_obj.author.unique_id}/video/{post_obj.video_id}"
        # url = "https://google.com"
        browser_session.solve_captcha_for_other_sessions(url)
        
        tasks = []
        for item in itemList:
            post_obj = Post(item, browser_session)
            task = asyncio.create_task(post_obj.fetchPostWithComments())
            tasks.append(task)
        
        results = await asyncio.gather(*tasks)
        return results
    else:
        return []


posts = asyncio.run(fetch_fasion_trending_posts(30))

print(len(posts))
if(len(posts)>0):
    print(posts[2].hashtags.titles)
    # print(posts[0].comments.titles)

# Close the session when done
# session.close_session()