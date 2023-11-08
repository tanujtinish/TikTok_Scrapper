
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.services.tiktok_recommendation_browser_session import TiktTokRecommendationBrowserSession

from src.database.models.posts import Posts

import asyncio

# Example usage:
ms_token = "K0A_4yeeT2o4VZRofZzNhSGGjrstUFiE6FCrG9jtOWTKP_XtPFuCadkKj7yxbUNNNbNtPidJtBx62VwudNXJRHA_TEp5ZTxOZgi0jzy7Tzvv1WOjNR3CnhiPHDROJFcROQ5UT8WaRnPmb9cP"
session = TiktTokRecommendationBrowserSession(ms_token)
posts = Posts(session)
asyncio.run(posts.parse_response())


print(len(posts.posts))
if(len(posts.posts)>0):
    print(posts.posts[2].hashtags.titles)
    # print(posts.posts[0].comments.titles)

# Close the session when done
# session.close_session()