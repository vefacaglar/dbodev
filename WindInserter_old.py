import xlrd
from datetime import datetime
import pymongo

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

lastYear = 0
lastMonth = 0
lastDay = 0
lasthour = 0

# veritabanına aktarılacak datalar ayarlanıyor.
for item in data:
    if item["Gün"]:
        day = "%02d" % int(item["Gün"])
        lastDay = day
    else:
        day = lastDay

    if item["Ay"]:
        month = "%02d" % int(item["Ay"])
        lastMonth = month
    else:
        month = lastMonth

    if item["Yıl"]:
        year = item["Yıl"]
        lastYear = year
    else:
        if(lastMonth == 12 and lasthour == 31):
            year += lastYear
        else:
            year = lastYear

    if item["Saat (UTC)"]:
        hour = "%02d" % int(item["Saat (UTC)"])
        lasthour = hour
    else:
        if(lasthour == 23):
            hour = 0
        else:
            hour += lasthour
    date = "{}-{}-{} {}:00".format(year, month, day, hour)
    # print(date)
    if item["Hiz"]:
        windsplit = item["Hiz"].replace("  ", " ").split(" ")
        windSpeed = windsplit[0]
        windDirection = windsplit[1]
        # print(windSpeed, windDirection)
    else:
        windSpeed = ""
        windDirection = ""

    newData = {
        "Date": date,
        "Windspeed": windSpeed,
        "Direction": windDirection
    }
    insertData.append(newData)
    print(newData)

mongoClient = pymongo.MongoClient("mongodb://localhost:27017/")
db = mongoClient["Homework"]
windData = db["WindData"]

# mongo ya insert ediyorum.
# windData.insert(insertData)
