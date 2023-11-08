import pymongo

connection_string = "mongodb://localhost:27017/"
database_name = "TikTok"
collection_name = "fasion_posts"

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
fasion_posts_collection = client[collection_name]