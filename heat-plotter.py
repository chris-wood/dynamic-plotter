import datetime
import random
import time
import plotly
import plotly.plotly as py
import plotly.tools as tls
from plotly.graph_objs import *
import tailer

keyfile = open("plotly.key", "r")
lines = keyfile.readlines()
lines = map(lambda x : x.strip(), lines)

py.sign_in(lines[0], lines[1])

import numpy as np  # (*) numpy for math functions and arrays

tls.set_credentials_file(stream_ids=lines[2:])

stream_ids = tls.get_credentials_file()['stream_ids']
print stream_ids

heatStreamId = stream_ids[1]

heatmap = Surface(stream=Stream(token=heatStreamId))
plot_data = Data([heatmap])
py.plot(plot_data)

x = 100
y = 100
numNodes = 100
get_data = lambda: np.random.randn(x, y) # creates a random 2D matrix

s = py.Stream(heatStreamId)
s.open()
n_frames = 1000
zz = np.empty([x, y])
for _ in xrange(n_frames):

    f = open("out.csv", "r")
    lines = tailer.tail(f, numNodes) # there are 5 nodes...
    for line in lines:
        line = line.split(",")
        div = int(line[0])
        x = int(line[1])
        y = int(line[2])
        val = float(line[3]) * -1

        # print len(zz)
        zz[x,y] = val
        print div,x,y,val
    s.write(dict(z=zz, type='surface'))

    time.sleep(1) # every second to see it evolve
s.close()
