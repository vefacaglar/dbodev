import pymongo

class MongoConnector: 
    def __init__ (self,connString = "mongodb://localhost:27017/", dbName = "Homework"):
        self.connString = connString
        self.dbName = dbName

    def Column(self,columnName):
        client = pymongo.MongoClient(self.connString)
        db = client[self.dbName]
        return db[columnName]