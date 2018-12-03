from Models.Numbers import Numbers
from Db.MongoConnector import MongoConnector
import pymongo

numbers = Numbers()
context = MongoConnector()
col = context.Column(numbers.CollectionName())

totalCount = col.find().count()
sumNumber = 0

print("total data sayısı", totalCount)

minNumber = col.find_one(sort=[("number", 1)])
print("min number",minNumber)

maxNumber = col.find_one(sort=[("number", -1)])
print("max number",maxNumber)

for number in range(16):
    query = {
        "number": number
    }
    numberCount = col.find(query).count()
    percent = (numberCount / totalCount) * 100
    sumNumber += (number * numberCount)
    print("numara {} adeti: {}, yüzde olarak: %{}".format(
        number, numberCount, "%.2f" % percent))

print("toplam:",sumNumber)
print("Ortalama: {}".format( "%.2f" % (sumNumber / totalCount)))
