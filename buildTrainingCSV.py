from datetime import datetime, timedelta
from os import path
from random import sample
from math import ceil
from normArchiveTemps import normSave
from stationScraper import scrapeStation

def nDayHistory(n):
    if not path.exists('3A25P_Archive.csv'):
        scrapeStation('3A25P Squamish River Upper')

    if not path.exists('3A22P_Archive.csv'):
        scrapeStation('3A22P Nostetuko River')

    if not (path.exists('3A25P_Archive_normed.csv') and path.exists('3A22P_Archive_normed.csv')):
        normSave()

    archiveData = {}
    with open('3A22P_Archive_normed.csv', 'r') as s1:
        with open('3A25P_Archive_normed.csv', 'r') as s2:
            _ = s1.readline()
            _ = s2.readline()
            l1 = s1.readline().strip('\n').split(',')
            l2 = s2.readline().strip('\n').split(',')
            while len(l1) > 1 and len(l2) > 1:
                if l1[0] < l2[0]:
                    l1 = s1.readline().strip('\n').split(',')
                if l1[0] > l2[0]:
                    l2 = s2.readline().strip('\n').split(',')
                else:
                    archiveData[l1[0]] = l1[1:] + l2[1:]
                    l1 = s1.readline().strip('\n').split(',')
                    l2 = s2.readline().strip('\n').split(',')
    dangerDict = {}
    with open('danger_ratings.csv', 'r') as dr:
        for line in dr:
            day,rate = line.strip('\n').split(',',1)
            dangerDict[day] = rate
    dangerDict = { key:value for (key,value) in dangerDict.items() if value != '-1' }
    prev = None
    outputRows = [[]]
    for offset in range(0,n+1):
        d = str(offset)
        outputRows[0] += ['S1_total_'+d,'S1_delta_'+d,'S1_min_'+d, 'S1_max_'+d, 'S1_mean_'+d]
        outputRows[0] += ['S2_total_'+d,'S2_delta_'+d,'S2_min_'+d, 'S2_max_'+d, 'S2_mean_'+d]
    outputRows[0] += ['Danger Rating']
    for key in sorted(archiveData.keys()):
        curr = datetime.strptime(key, '%Y-%m-%d')
        firstDay = datetime.strftime(curr - timedelta(days = n), '%Y-%m-%d')
        if firstDay in archiveData and key in dangerDict:
            outputRows.append([])
            for offset in range(0,n+1):
                outputRows[-1] += archiveData[datetime.strftime(curr - timedelta(days = offset), '%Y-%m-%d')]
            outputRows[-1] += [dangerDict[key]]
    validation_rows = sample(outputRows[1:], ceil(len(outputRows[1:])*0.05))
    with open('snowFallData/valSet_N_'+str(n)+'.csv', 'w') as valfile:
        valfile.write(','.join(outputRows[0])+'\n')
        with open('snowFallData/dataSet_N_'+str(n)+'.csv', 'w') as outfile:
            for row in outputRows:
                if row in validation_rows:
                    valfile.write(','.join(row)+'\n')
                else:
                    outfile.write(','.join(row)+'\n')

if __name__ == '__main__':
    nDayHistory(0)
    nDayHistory(1)
    nDayHistory(2)
    nDayHistory(3)
