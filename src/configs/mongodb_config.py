import pymongo

connection_string = "mongodb+srv://finesse:tiktok_challenge@cluster0.z6rbtcz.mongodb.net/"
database_name = "TikTok"

def connect_to_mongodb():
    try:
        client = pymongo.MongoClient(connection_string)
        db = client[database_name]
        app.logger.info("Connected to MongoDB")
        return db
    except Exception as e:
        app.logger.info("Error connecting to MongoDB: ", e)
        return None
    
client = connect_to_mongodb()
scraped_posts_collection = client["scraped_posts"]
scraped_posts_with_comments_collection = client["scraped_posts_with_comments"]
fasion_posts_collection = client["fasion_posts"]