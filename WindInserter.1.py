import xlrd
from datetime import datetime
from datetime import timedelta
import pymongo
import random

file = "veri.xlsx"

workbook = xlrd.open_workbook(file)
worksheet = workbook.sheet_by_index(0)

# başlıkları çekiyorum
first_row = []
for col in range(worksheet.ncols):
    first_row.append(worksheet.cell_value(0, col))

# excel datalarını topluyorum
data = []
for row in range(1, worksheet.nrows):
    elm = {}
    for col in range(worksheet.ncols):
        elm[first_row[col]] = worksheet.cell_value(row, col)
    data.append(elm)

# tüm dataların toplanması için boş bir dizi oluşturuyorum.
insertData = []

firstDate = datetime(2011, 1, 1, 0)
lastDate = datetime(2012, 12, 31, 23)

datesDate = []
# iki tarih aralığındaki tüm saatleri eksiksiz bir şekilde mongo ya basıyorum
while firstDate <= lastDate:
    # print(firstDate)
    firstDate = firstDate + timedelta(hours=1)
    newData = {
        "Date": firstDate,
        "Windspeed": "",
        "Direction": ""
    }
    datesDate.append(newData)

mongoClient = pymongo.MongoClient("mongodb://localhost:27017/")
db = mongoClient["Homework"]
windData = db["WindData2"]
# tüm tarihlerin mognoya basıldığı kısım
windData.insert(datesDate)

# rüzgar hızı olan datalar mongoya update ediliyor.
for item in data:
    if item["Gün"]:
        day = int(item["Gün"])

    if item["Ay"]:
        month = int(item["Ay"])

    if item["Yıl"]:
        year = int(item["Yıl"])

    if item["Saat (UTC)"]:
        hour = int(item["Saat (UTC)"])

    date1 = datetime(year, month, day, hour)

    dateQuery = {
        "Date": date1
    }

    if item["Hiz"]:
        windsplit = item["Hiz"].replace("  ", " ").split(" ")
        windSpeed = windsplit[0]
        windDirection = windsplit[1]
        # print(windSpeed, windDirection)
    else:
        windSpeed = ""
        windDirection = ""

    newData = {
        "Date": date1,
        "Windspeed": windSpeed,
        "Direction": windDirection
    }

    windData.update_one({
        'Date': date1
    }, {
        '$set': {
            'Windspeed':windSpeed,
            "Direction": windDirection
        }
    }, upsert=False)
    print(date1,"rüzgar bilgisi update ediliyor")
    #insertData.append(newData)
    #print(newData)

windList = windData.find({})

for item in windList:
    if(not item['Windspeed']):
        lastDate = item['Date']
        last10data = windData.find({
            "Windspeed": {"$ne": ''},
            "Date": {
                "$lt": lastDate
            }
        }).limit(10).sort("Date", pymongo.DESCENDING)

        last10speed = []
        last10direction = []
        for wind in last10data:
            last10speed.append(wind["Windspeed"])
            last10direction.append(wind["Direction"])

        randomSpeed = random.choice(last10speed)
        randomDirection = random.choice(last10direction)
        print(randomSpeed, randomDirection,"tahmin edilen rüzgar bilgisi")

        windData.update_one({
            'Date': lastDate
        }, {
            '$set': {
                'Windspeed': randomSpeed,
                "Direction": randomDirection
            }
        }, upsert=False)


#mongoClient = pymongo.MongoClient("mongodb://localhost:27017/")
#db = mongoClient["Homework"]
#windData = db["WindData"]

# mongo ya insert ediyorum.
#windData.insert(insertData)
