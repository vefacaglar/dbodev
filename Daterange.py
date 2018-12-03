from datetime import date, timedelta,datetime

firstDate = datetime(2011,1,1,0)
lastDate = datetime(2012,12,31,23)

print(firstDate)
print(lastDate)

while firstDate <= lastDate:
    print(firstDate)
    firstDate = firstDate + timedelta(hours=1)