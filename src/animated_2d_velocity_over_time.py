import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as ani
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# This script creates an animated 2D chart gif from the data of a .csv file. 
# The original use case was to demonstrate the speed differences between two cars in a drag race, but it can animate any sort of .csv data.

file_path = '../other/speed_comparison.csv'
gif_path = r'..\visuals\animated_2d_velocity_over_time.gif'

# read in data
df1 = pd.read_csv(file_path, delimiter=',', header=0)

# configure graph
plt.style.use('dark_background')
color = ['#f72585', '#4361ee', '#b5179e', '#4895ef', '#7209b7', '#4cc9f0']
fig = plt.figure(figsize=(10, 6))
plt.xticks(rotation=45, ha="right", rotation_mode="anchor") # rotate the x-axis values
plt.subplots_adjust(bottom = 0.2, top = 0.9) # ensuring the data (on the x-axis) fits inside the screen
plt.ylabel('Speed (m/s)')
plt.xlabel('Time (ms * 10)')

# build graph
def buildmebarchart(i=int):
    plt.legend(df1.columns)
    p = plt.plot(df1[:i].index, df1[:i].values) # note it only returns the dataset, up to the point i
    for i in range(0,6):
        p[i].set_color(color[i]) # set the color of each curve

# create animation
import matplotlib.animation as ani
animator = ani.FuncAnimation(fig, buildmebarchart, interval = 100)

# save animation as a gif
animator.save(gif_path)

# show graph
plt.show()