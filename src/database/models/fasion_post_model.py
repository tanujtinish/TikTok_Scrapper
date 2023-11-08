import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from src.services.mongodb_service import Mongodb_service
from src.configs.mongodb_opl_config import website_collection

class Website_link_model:
  def __init__(self, web_url, crawled):
    self.website_url = web_url
    self.crawl_status = crawled
    self.mongodbservice = Mongodb_service(website_collection)

  def save(self):
    try:
      if(self.website_url):
        self.mongodbservice.save_to_mongodb({"website_url": self.website_url,"crawled":self.crawl_status})
      else:
        raise Exception("No content to save")
    except Exception as e:
      print(e)
      raise Exception("Error saving content to MongoDB")