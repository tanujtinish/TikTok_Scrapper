import pymongo

connection_string = "mongodb://localhost:27017/"
database_name = "TikTok"

def connect_to_mongodb():
    try:
        client = pymongo.MongoClient(connection_string)
        db = client[database_name]
        print("Connected to MongoDB")
        return db
    except Exception as e:
        print("Error connecting to MongoDB: ", e)
        return None
    
client = connect_to_mongodb()
scraped_posts_collection = client["scraped_posts"]
scraped_posts_with_comments_collection = client["scraped_posts_with_comments"]
fasion_posts_collection = client["fasion_posts"]