import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import glob

# This script creates an interactive 3D chart of the racing line data from a specified folder.
# unfortunately, Plotly doesn't work super easily with animations, so this script will only output an interactive chart, not a .gif file.

# references
# https://plotly.com/python/animations/
# https://plotly.com/python/#animations
# https://plotly.com/python/visualizing-mri-volume-slices/
# https://plotly.com/python/animations/

# path to folder containing the racing line files
folder_path = '../data/*csv'

# set the chart bounds
# these values should typically be ~10% bigger than the bounds of the paths you are drawing
# for instance, if a track has dimensions of 1000x1000x10 meters and is centered around the origin (0,0,0), then your bounds should be:
# x: -550, 550
# y: -550, 550
# x: -5.5, 5.5
map_bounds = dict(
        xaxis=dict(range=[-13000,10000]),
        yaxis=dict(range=[-13000,10000]),
        zaxis=dict(range=[-13000,10000])
)

# create and offset the racing line
def create_racing_line(filename, xOffset, yOffset, zOffset, color):
    df = pd.read_csv(filename,sep=',')
    return go.Scatter3d(
        x=df['PositionX'] + xOffset, # offset moves all the points by some amount and allows you to manually center a racing line in the chart
        y=df['PositionZ'] + yOffset, 
        z=df['PositionY'] + zOffset, 
        name=filename,
        line=dict(
            width=1,
            color=color
        ),
        marker=dict(
            size=1
        ))

# get data from each file in the specified folder
def load_files(folder_path):
    data_folder = glob.glob(folder_path)
    files = []
    for filename in data_folder:
        files.append(filename)
    return files

files = []
files += load_files(folder_path)

# create plot
fig = go.Figure()
fig.update_yaxes(gridwidth=0)
#fig.layout.template = 'plotly_dark' # enable for dark mode
fig.update_layout(scene=map_bounds)

# add data from each file in folder to the graph
for filename in files:
    if ("fh4" in filename): # example of how to turn a certain file's racing line data a different color and give it a different location on the graph
        fig.add_trace(create_racing_line(filename,0,0,0,'blue'))
    else: 
        fig.add_trace(create_racing_line(filename,0,0,0,'red'))

# show plot
fig.show()