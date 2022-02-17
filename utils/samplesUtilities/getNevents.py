
from nevents_2017 import data

tot = 0

for key in data.keys():
  tot += int(data[key][0]["nevents"])


print 'Total number of events in list is ' , tot
