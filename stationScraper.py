from datetime import datetime
from statistics import mean

outputTitles = ['Date','Total Snow','Daily Delta','Min','Max','Mean']
outputRows = {}
dateformat = '%Y-%m-%d %H:%M'
start = datetime.strptime('2014-01-01 00:00', dateformat)
end   = datetime.strptime('2018-12-31 23:59', dateformat)
station = '3A25P Squamish River Upper'
with open('SWDaily_Archive.csv', 'r') as fullCSV:
    line = fullCSV.readline()
    titles = line.split(',')
    column = titles.index(station)
    line = fullCSV.readline()
    depth = 0
    while line:
        field = line.split(',')[column]
        currDS = line.split(',',1)[0]
        currDT = datetime.strptime(currDS, dateformat)
        if  currDT >= start and currDT <= end:
            prev = depth
            if len(field) > 0:
                depth = float(field)
            else:
                depth = 0
            outputRows[currDT.strftime('%Y-%m-%d')] = [str(depth), str(depth - prev)]
        line = fullCSV.readline()

with open('TA_Archive.csv', 'r') as hourlyCSV:
    line = hourlyCSV.readline()
    titles = line.split(',')
    column = titles.index(station)
    line = hourlyCSV.readline()
    preday = ''
    TA_list = []
    while line:
        field = line.split(',')[column]
        currDS = line.split(',',1)[0]
        currDT = datetime.strptime(currDS, dateformat)
        if  currDT >= start and currDT <= end:
            today = currDT.strftime('%Y-%m-%d')
            if today == preday:
                TA_list.append(float(field) if len(field) > 0 else 0.0)
            else:
                if preday in outputRows and len(TA_list):
                    outputRows[preday] += [str(min(TA_list)),str(max(TA_list)),str(mean(TA_list))]
                    TA_list = []
                preday = today
        if currDT > end and len(TA_list):
            outputRows[today] += [str(min(TA_list)),str(max(TA_list)),str(mean(TA_list))]
            TA_list = []
        line = hourlyCSV.readline()

with open(station.split(' ',1)[0]+'_Archive.csv', 'w') as outCSV:
    outCSV.write(','.join(outputTitles) + '\n')
    for day in outputRows:
        outCSV.write(day+','+','.join(outputRows[day])+'\n')
