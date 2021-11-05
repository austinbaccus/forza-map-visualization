import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation
import pandas as pd
import glob

# This script creates an animated 3D gif of the racing line data from a specified folder.

folder_path = '../data/*csv'
gif_path = r'..\visuals\animated_3d_racing_lines.gif'

def update_line(num, data, line):
    line.set_data(data[0:2, :num])    
    line.set_3d_properties(data[2, :num])    
    return line

def update_lines(num, data, lines):
    for line, data in zip(lines, data):
        line.set_data(data[0:2, :num])
        line.set_3d_properties(data[2, :num])
    return lines

def make_line(filename, bounds):    
    repo = pd.read_csv(filename,sep=',',header=0)
    set_axis(ax, bounds)
    data = np.array((repo['PositionX'].values, repo['PositionZ'].values, repo['PositionY'].values))
    return data

def set_axis(ax,bounds):
    ax.set_xlim3d([bounds[0], bounds[3]]) # length
    ax.set_ylim3d([bounds[2], bounds[5]]) # width
    ax.set_zlim3d([bounds[1], bounds[4]]) # height
    ax.set_ylabel('Y')
    ax.set_xlabel('X')
    ax.set_zlabel('Z')
    
def get_bounds(data_folder):
    # keep track of the min and max values for each dimension
    minX = 0
    minY = 0
    minZ = 0
    maxX = 0
    maxY = 0
    maxZ = 0
    firstFile = True
    
    # get the minimum and maximum dimension values across every file
    for filename in data_folder:
        repo = pd.read_csv(filename,sep=',',header=0)

        localMinX = min(repo['PositionX'].values)
        localMinY = min(repo['PositionY'].values)
        localMinZ = min(repo['PositionZ'].values)
        localMaxX = max(repo['PositionX'].values)
        localMaxY = max(repo['PositionY'].values)
        localMaxZ = max(repo['PositionZ'].values)

        if firstFile or localMinX < minX:
            minX = localMinX
        if firstFile or localMinY < minY:
            minY = localMinY
        if firstFile or localMinZ < minZ:
            minZ = localMinZ
        if firstFile or localMaxX > maxX:
            maxX = localMaxX
        if firstFile or localMaxY > maxY:
            maxY = localMaxY
        if firstFile or localMaxZ > maxZ:
            maxZ = localMaxZ

        firstFile = False

    l = maxX - minX
    w = maxZ - minZ

    # make the length and width of the graph the same amount so that there's no stretching
    if l < w:
        diff = w - l
        minX = minX - (diff/2)
        maxX = maxX + (diff/2)
    if l > w:
        diff = l - w
        minZ = minZ - (diff/2)
        maxZ = maxZ + (diff/2)

    # increase the height of the chart relative to the actual height difference so that Top Gear doesn't look like it's nestled in a mountain valley
    h = maxY - minY
    maxY = maxY + (h * 1.25)
    minY = minY - (h * 1.25)

    return [minX, minY, minZ, maxX, maxY, maxZ]

# Attaching 3D axis to the figure
plt.style.use('seaborn')
fig = plt.figure()
ax = p3.Axes3D(fig)

# grab racing lines from the data folder
data_folder = glob.glob(folder_path)
dataList = []
maxCount = 0
bounds = get_bounds(data_folder)

for filename in data_folder:
    m = make_line(filename, bounds)
    dataList.append(m)
    maxCount = max(maxCount, len(m[0]))

# make all data items (3D racing lines) equal length (same amount of rows) so that python doesn't throw a fit
for i in range(len(dataList)):
    if len(dataList[i][0]) < maxCount:
        old_end_idx = len(dataList[i][0]) - 1
        rows_to_fill = maxCount - len(dataList[i][0])
        x = dataList[i][0][old_end_idx]
        y = dataList[i][1][old_end_idx]
        z = dataList[i][2][old_end_idx]
        for j in range(rows_to_fill):
            new_row = np.array([x,y,z])
            dataList[i] = np.column_stack((dataList[i],new_row))

data = np.array(dataList, dtype=object)

# get all racing lines from the data
lines = [ax.plot(dat[0, 0:1],  dat[1, 0:1],  dat[2, 0:1])[0] for dat in data]

# create animation
line_ani = animation.FuncAnimation(fig, update_lines, data[0].shape[1], fargs=(data, lines), interval=1, blit=False)

# save gif
line_ani.save(gif_path, writer=animation.PillowWriter(fps=60))

# show graph
plt.show()