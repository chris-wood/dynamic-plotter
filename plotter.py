import plotly
import plotly.plotly as py  
import plotly.tools as tls   
from plotly.graph_objs import *

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

# (@) Open the stream
s.open()

# (*) Import module keep track and format current time
import datetime
import time

i = 0    # a counter
k = 5    # some shape parameter
N = 200  # number of points to be plotted

# Delay start of stream by 5 sec (time to switch tabs)
time.sleep(5)

while i<N:
    i += 1   # add to counter

    # Current time on x-axis, random numbers on y-axis
    x = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    y = (np.cos(k*i/50.)*np.cos(i/50.)+np.random.randn(1))[0]

    # (-) Both x and y are numbers (i.e. not lists nor arrays)

    # (@) write to Plotly stream!
    s.write(dict(x=x, y=y))

    # (!) Write numbers to stream to append current data on plot,
    #     write lists to overwrite existing data on plot (more in 7.2).

    time.sleep(0.08)  # (!) plot a point every 80 ms, for smoother plotting

# (@) Close the stream when done plotting
s.close()
