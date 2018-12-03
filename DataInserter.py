import random
import pymongo

mongoClient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = mongoClient["Homework"]
mycol = mydb["numbers"]

dataModel = []

for x in range(100000):
    randomNumber = random.randint(0,15)
    print(x, ": ",randomNumber," kaydedildi")
    insertValue = {
        "index": x,
        "number": randomNumber
        }
    dataModel.append(insertValue)

##mycol.insert(dataModel) 

print(mycol)