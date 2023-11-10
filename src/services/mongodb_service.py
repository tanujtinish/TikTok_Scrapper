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

  def update_batch(self, ids):
    self.collection.update_many({"_id": {"$in": ids}}, {"$set": {"": ""}})

  def find_by_id(self, id):
    res = self.collection.find_one({"_id": id})
    return res