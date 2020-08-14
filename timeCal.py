import datetime
import math

index_int = 0
for index in range(36):
  time_stamp = datetime.datetime.now() + datetime.timedelta(hours = index * 1 + index_int * 10 + 2.2)
  hours = int(time_stamp.strftime('%H'))
  print(index_int)
  if hours > 22 or hours < 9:
    index_int = index_int + 1
    time_stamp = datetime.datetime.now() + datetime.timedelta(hours = index * 1 + index_int * 10 + 2.2)
  print('预定的发布时间：' + time_stamp.strftime('%Y-%m-%d %H:%M'))