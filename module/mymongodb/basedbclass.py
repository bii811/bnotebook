from pymongo import MongoClient
import pymongo.errors
from bson import ObjectId
import time


class BaseMongoDB:
    HOST = "192.168.99.100"
    PORT = 32777
    database_name = "b_notebook"

    def __init__(self, collection_name=None, _id=None, modified_date=None):
        self.client = MongoClient(self.HOST, self.PORT, serverSelectionTimeoutMS=1000, connect=False)
        self.database = self.client[self.database_name]
        self.collection = self.database[str(collection_name)]

        self.id = _id
        self.created_date = None
        self.modified_date = modified_date

        self.set_created_date()

    def check_connection(self):
        try:
            self.client.admin.command('ismaster')
        except pymongo.errors.ConnectionFailure:
            print("Server not available")

    def set_created_date(self):
        if self.id:
            self.created_date = ObjectId(self.id).generation_time

    def set_modified_date(self):
        self.modified_date = time.time()

    def find(self, filter_document):
        result = self.collection.find(filter_document)
        print("[DB][Find]: {}".format(result.count()))

    def insert(self, document):
        self.set_modified_date()
        document['modified_date'] = self.modified_date
        self.collection.insert_one(document)
        print("[DB][InsertedOne]: {}".format(document))

    def delete(self):
        result = self.collection.delete_one({'_id': self.id})
        print("[DB][DeletedOne]: {} {}".format(result.deleted_count, self.id))

    def update(self, update_document):
        result = self.collection.update_one({'_id': self.id}, {'$set': update_document})
        print("[DB][UpdatedOne]: {}".format(result.raw_result))

