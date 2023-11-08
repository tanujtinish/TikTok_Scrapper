import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.configs.mongodb_config import client

class Mongodb_service:
  def __init__(self, collection_name):
    self.client = client
    self.collection = collection_name

  def save_to_mongodb(self, data):
    self.collection.insert_one(data)
  
  def save_to_mongodb_return_id(self, data):
    return self.collection.insert_one(data).inserted_id
  
  def save_many_to_mongodb(self, data):
    self.collection.insert_many(data)

  def get_all_crawed_data(self):
    res = self.collection.find({"status": "C"})
    return res
  
  def update_status_batch(self, ids):
    self.collection.update_many({"_id": {"$in": ids}}, {"$set": {"status": "T"}})
    print("Updated status to T")

  def find_by_id(self, id):
    res = self.collection.find_one({"_id": id})
    return res

  def get_all_uncrawled_websites(self):
    res = self.collection.find({"crawled": "Pending"}).limit(10)
    return res
  
  def set_crawled_website(self, url):
    self.collection.update_one({"website_url": url}, {"$set": {"crawled": "Crawled"}})
    print("Updated status to Crawled")