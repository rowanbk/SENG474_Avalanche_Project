with open('SWDaily_Archive.csv', 'r') as fullCSV:
    outputRows = [['Date','Total Snow','Daily Delta']]
    line = fullCSV.readline()
    titles = line.split(',')
    column = titles.index('3A25P Squamish River Upper')
    line = fullCSV.readline()
    depth = 0
    while line:
        field = line.split(',')[column]
        prev = depth
        if len(field) > 0:
            depth = float(field)
        else:
            depth = 0
        outputRows.append([line.split(',',1)[0], str(depth), str(depth - prev)])
        line = fullCSV.readline()

with open('3A25P_Archive.csv', 'w') as outCSV:
    for line in outputRows:
        outCSV.write(','.join(line) + '\n')
