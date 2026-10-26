import numpy as np

dataRaw = []
with open('data/static.dat', 'r') as f:
    for line in f:
        dataRaw.append(line.strip())

data = np.array([ 0, 0, 0, 0, 0, 0, 0, 0])
for line in dataRaw:
    data = np.vstack((data, np.array([float(it) for it in line.split()])))

data = data[1:, :]
times = data[:, 1]

dt = np.diff(times)
avgDt = np.sum(dt)/len(dt)

# acc analysis
ax = data[:, 2]
ay = data[:, 3]
az = data[:, 4]

acc = data[:, 2:5]
accNorm = np.linalg.norm(acc, axis=1)



gx = data[:, 5]
gy = data[:, 6]
gz = data[:, 7]