# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


#class MoviesPipeline(object):
#    def process_item(self, item, spider):
#        return item

import pymongo
import settings
from scrapy.exceptions import DropItem

class MongoDBPipeline(object):
  
   def __init__(self):
      connection = pymongo.MongoClient(
         settings.MONGODB_SERVER,
         settings.MONGODB_PORT)

      db = connection[settings.MONGODB_DB]
      self.collection = db[settings.MONGODB_COLLECTION]

   def process_item(self,item,spider):

      valid = True
      for data in item:
         if not data:
            valid = False
            raise DropItem("Miss {0}".format(date))
      if valid:
         self.collection.insert(dict(item))
      return None


