from shapely.geometry import Polygon
import pandas as pd
import glob

# load csv files in target folder
def load_files(folder_path):
    data_folder = glob.glob(folder_path)
    files = []
    for filename in data_folder:
        files.append(filename)
    return files

# specify folder containing the relevant data
folder_path = '../loops/*csv'

# add file data to list
files = []
files += load_files(folder_path)

# extract XYZ coordinate data from CSV file
def get_data(filename):
    df = pd.read_csv(filename,sep=',')
    x=df['PositionX']
    y=df['PositionY']
    z=df['PositionZ']
    return (x, y, z)

# calculate area for each file
for filename in files:
    data = get_data(filename)
    pgon = Polygon(zip(data[0], data[2]))
    print(filename, pgon.area/1000)