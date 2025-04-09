from pymongo import MongoClient

class MongoDBLoader:
    def __init__(self, mongo_uri, db_name):
        self.client = MongoClient(mongo_uri)
        self.db = self.client[db_name]

    def load_documents(self, documents, collection_name):
        """
        Lưu trữ danh sách documents vào MongoDB.
        :param documents: List of dictionaries to insert.
        :param collection_name: Name of the MongoDB collection.
        """
        collection = self.db[collection_name]
        collection.insert_many(documents)
        print(f"✅ Saved {len(documents)} documents to MongoDB collection: {collection_name}")