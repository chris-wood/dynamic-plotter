import datetime
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

stream_id = stream_ids[0]

stream = Stream(
    token=stream_id,  # (!) link stream id to 'token' key
    maxpoints=80      # (!) keep a max of 80 pts on screen
)

trace1 = Scatter(
    x=[],
    y=[],
    mode='lines+markers',
    stream=stream         # (!) embed stream id, 1 per trace
)

data = Data([trace1])

layout = Layout(title='Time Series')

# Make a figure object
fig = Figure(data=data, layout=layout)

# (@) Send fig to Plotly, initialize streaming plot, open new tab
unique_url = py.plot(fig, filename='s7_first-stream')

s = py.Stream(stream_id)

s.open()

i = 0    # a counter
k = 5    # some shape parameter
N = 200

# Delay start of stream by 5 sec (time to switch tabs)
time.sleep(5)

while i<N:
    # go forever
    # i += 1

    # TODO: scan for new files, send them to new streams
    f = open("out.csv", "r")
    lines = tailer.tail(f, 1)

    seenX = []
    for line in lines:
        line = line.split(",")
        x = datetime.datetime.fromtimestamp(float(line[0]) / 1000.0)
        if x not in seenX:
            seenX.append(x)
            y = float(line[1])
            s.write(dict(x=x, y=y))
            print "writing %s" % (str(dict(x = x, y = y)))

    time.sleep(0.08)

s.close()
