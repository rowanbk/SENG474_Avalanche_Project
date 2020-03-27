from sklearn.preprocessing import MinMaxScaler
import numpy as np

def normSave():
    with open('3A22P_Archive.csv', 'r') as s1:
        with open('3A25P_Archive.csv', 'r') as s2:
            pref = []
            totSnow = []
            deltaSnow = []
            temps = []

            header = s1.readline()
            line = s1.readline().strip('\n').split(',')
            s1Count = 0
            while len(line) > 1:
                pref.append(line[0])
                totSnow.append(float(line[1]))
                deltaSnow.append(float(line[2]))
                temps.append([float(t) for t in line[3:]])
                line = s1.readline().strip('\n').split(',')
                s1Count += 1

            _ = s2.readline()
            line = s2.readline().strip('\n').split(',')
            while len(line) > 1:
                pref.append(line[0])
                totSnow.append(float(line[1]))
                deltaSnow.append(float(line[2]))
                temps.append([float(t) for t in line[3:]])
                line = s2.readline().strip('\n').split(',')

            totSnow = np.asarray(totSnow).reshape(-1, 1)
            scaler = MinMaxScaler().fit(totSnow)
            scaled_total = np.squeeze(scaler.transform(totSnow)).tolist()

            deltaSnow = np.asarray(deltaSnow).reshape(-1, 1)
            scaler = MinMaxScaler().fit(deltaSnow)
            scaled_delta = np.squeeze(scaler.transform(deltaSnow)).tolist()

            scaler = MinMaxScaler().fit(temps)
            scaled_temps = scaler.transform(temps).tolist()
    with open('3A22P_Archive_normed.csv', 'w') as out:
        out.write(header)
        for line in zip(pref[:s1Count], scaled_total[:s1Count], scaled_delta[:s1Count], scaled_temps[:s1Count]):
            out.write(','.join(str(item) for item in list(line[:3])+line[3]) + '\n')
    with open('3A25P_Archive_normed.csv', 'w') as out:
        out.write(header)
        for line in zip(pref[s1Count:], scaled_total[s1Count:], scaled_delta[s1Count:], scaled_temps[s1Count:]):
            out.write(','.join(str(item) for item in list(line[:3])+line[3]) + '\n')

if __name__ == '__main__':
    normSave()
