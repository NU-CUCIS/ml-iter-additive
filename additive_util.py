import pandas as pd
import numpy as np
import warnings
import math
import time
import json
import os
from numpy import save,load

DEFAULT_TEMP = 300
NON_EXISTING_TEMP = -99

def modLog(num):
    """
    Returns log if it exist, else returns 0
    """
    try:
        return log(num)
    except:
        return 0

def loadNumpy(name,path='.'):
    """
    Loads numpy file
    - If no path is provided, the home directory . is considered
       as default path of numpy file
    """
    if ".npy" in name:
        fullPath = path+'/'+name
    else:
        fullPath = path+'/'+name+'.npy'
    return load(fullPath)


def saveNumpy(obj, name, path='.'):
    """
    Saves numpy file
    """
    if ".npy" not in name:
        fullPath = path+'/'+name
        save(fullPath, obj)
        print name,'saved successfully in',path
    else:
        fullPath = path+'/'+name.split(".npy")[0]
        save(fullPath, obj)
        print name,'saved successfully in',path


def loadDict(name,path='.'):
    """
    Load Pickle Dictionary 
    """
    if ".dict" not in name:
        name += '.dict'

    if ".npy" in name:
        fullPath = path+'/'+name
    else:
        fullPath = path+'/'+name+'.npy'
    return load(fullPath).tolist()


def saveDict(obj, name, path='.'):
    if ".dict" not in name:
        fullPath = path+'/'+name+'.dict'
        save(fullPath, obj)
        print name,'saved successfully in',path
    else:
        fullPath = path+'/'+name
        save(fullPath, obj)
        print name,'saved successfully in',path

dataframe = df = pd.read_csv('data/data_big.csv',header=None)
indices = loadDict('indices_big')

def front(self, n):
    return self.iloc[:, :n]

def back(self, n):
    return self.iloc[:, -n:]

pd.DataFrame.front = front
pd.DataFrame.back = back

def parse_toolpath(FolderName,FileName,dt):
    complete_filename = os.path.join(FolderName,FileName)
    toolpath_raw=pd.read_table(complete_filename,delimiter=r"\s+",header=None, names=['time','x','y','z','state'])
    toolpath=[]
    state=[]
    time=0.0
    ind=0
    endTime = float(toolpath_raw.tail(1)['time'])
    while(time<=endTime):
        while(time>=toolpath_raw['time'][ind+1]):
            ind=ind+1
        X=toolpath_raw['x'][ind]+(toolpath_raw['x'][ind+1]-toolpath_raw['x'][ind])*(
            time-toolpath_raw['time'][ind])/(toolpath_raw['time'][ind+1]-toolpath_raw['time'][ind])
        Y=toolpath_raw['y'][ind]+(toolpath_raw['y'][ind+1]-toolpath_raw['y'][ind])*(
            time-toolpath_raw['time'][ind])/(toolpath_raw['time'][ind+1]-toolpath_raw['time'][ind])
        Z=toolpath_raw['z'][ind]+(toolpath_raw['z'][ind+1]-toolpath_raw['z'][ind])*(
            time-toolpath_raw['time'][ind])/(toolpath_raw['time'][ind+1]-toolpath_raw['time'][ind])
        toolpath.append([X,Y,Z])
        state.append(toolpath_raw['state'][ind+1])
        time = time +dt
    return toolpath, state, endTime

class Coordinate(object):
    """
    Class for treating voxels in 3-D coordinates
    """
    def __init__(self, x,y,z ):
        self.X = x
        self.Y = y
        self.Z = z

    def __str__(self):
        return "Coordinate(%s,%s,%s)"%(self.X, self.Y, self.Z)

    def getX(self):
        return self.X

    def getY(self):
        return self.Y

    def getZ(self):
        return self.Z

    def getXYZ(self):
        return self.X, self.Y, self.Z

    def distance(self, other):
        dx = self.X - other.X
        dy = self.Y - other.Y
        dz = self.Z - other.Z
        return math.sqrt(dx**2 + dy**2 + dz**2)

def getTemperatureInit(p):
    """
    Initializes the temperature of a voxel
    - If a temperature does not exist, it sets it with a default temperature NON_EXISTING_TEMP
    """
    xyzTuple = p.getXYZ()
    if xyzTuple in indices.keys():
        return valueDict[xyzTuple][1]
    else:
        return NON_EXISTING_TEMP

def getTemperature(p,timestep):
    """
    Extracts the temperature of a point
    - If it does not exist, it is set to a default temperature
    """
    xyzTuple = p.getXYZ()
    if xyzTuple in indices.keys() and timestep>0:
        dfIndex = indices[xyzTuple]
        temp_timestep = dataframe.loc[dfIndex].tolist()[timestep+4]
        return temp_timestep
    else:
        return NON_EXISTING_TEMP

def findNeighbors(p):
    """
    It extracts the neighbors of a given voxel
    """
    neighbors = []
    ### immediate/adjacent neighbors - 1 degree
    neighbors+= [Coordinate(p.X - 0.5, p.Y, p.Z)]
    neighbors+= [Coordinate(p.X + 0.5, p.Y, p.Z)]

    neighbors+= [Coordinate(p.X, p.Y - 0.5, p.Z)]
    neighbors+= [Coordinate(p.X, p.Y + 0.5, p.Z)]

    neighbors+= [Coordinate(p.X, p.Y, p.Z - 0.5)]
    neighbors+= [Coordinate(p.X, p.Y, p.Z + 0.5)]

    ### distance - 2 degree
    neighbors+= [Coordinate(p.X - 0.5, p.Y - 0.5, p.Z)]
    neighbors+= [Coordinate(p.X - 0.5, p.Y + 0.5, p.Z)]
    neighbors+= [Coordinate(p.X + 0.5, p.Y - 0.5, p.Z)]
    neighbors+= [Coordinate(p.X + 0.5, p.Y + 0.5, p.Z)]

    neighbors+= [Coordinate(p.X, p.Y - 0.5, p.Z - 0.5)]
    neighbors+= [Coordinate(p.X, p.Y + 0.5, p.Z - 0.5)]
    neighbors+= [Coordinate(p.X, p.Y - 0.5, p.Z + 0.5)]
    neighbors+= [Coordinate(p.X, p.Y + 0.5, p.Z + 0.5)]

    neighbors+= [Coordinate(p.X - 0.5, p.Y, p.Z - 0.5)]
    neighbors+= [Coordinate(p.X + 0.5, p.Y, p.Z - 0.5)]
    neighbors+= [Coordinate(p.X - 0.5, p.Y, p.Z + 0.5)]
    neighbors+= [Coordinate(p.X + 0.5, p.Y, p.Z + 0.5)]

    ### diagonal neighbors distance - 3 degree
    neighbors+= [Coordinate(p.X - 0.5, p.Y - 0.5, p.Z - 0.5)]
    neighbors+= [Coordinate(p.X - 0.5, p.Y + 0.5, p.Z - 0.5)]
    neighbors+= [Coordinate(p.X + 0.5, p.Y - 0.5, p.Z - 0.5)]
    neighbors+= [Coordinate(p.X + 0.5, p.Y + 0.5, p.Z - 0.5)]

    neighbors+= [Coordinate(p.X - 0.5, p.Y - 0.5, p.Z + 0.5)]
    neighbors+= [Coordinate(p.X - 0.5, p.Y + 0.5, p.Z + 0.5)]
    neighbors+= [Coordinate(p.X + 0.5, p.Y - 0.5, p.Z + 0.5)]
    neighbors+= [Coordinate(p.X + 0.5, p.Y + 0.5, p.Z + 0.5)]

    return neighbors

def printNeighbors(p):
    """
    It prints the temperature of the neighbors
    """
    neighbors = findNeighbors(p)
    print "The neighbors of point",p," are:"
    print
    print "Immediate Neighbors: "
    print
    for i in range(0,6):
        print neighbors[i]

    print
    print "2-D diagonal Neighbors: "
    print
    for i in range(6,18):
        print neighbors[i]

    print
    print "3-D diagonal Neighbors: "
    print
    for i in range(18,26):
        print neighbors[i]

def createDictionaries(dataframe):
    """
    It creates a dictionary with keys as (x,y,z) and temperature as value
    """
    start = time.time()
    dictionaryIndices,dictionaryValues = {},{}
    for i in range(len(dataframe)):
        (x,y,z) = dataframe.loc[i][:3].tolist()
        key = (x,y,z)
        value = dataframe.loc[i][3:].tolist()
        dictionaryIndices[key] = i
        dictionaryValues[key] = value
    stop = time.time()
    print 'The time for dictionary creation is %2f seconds' %(stop-start)
    return dictionaryIndices,dictionaryValues


def findNeighborTemperatures(p,timestep=1):
    """
    Extracts the temperature of neighboring voxels
    - Timestep is considered as 1 by default
    """
    neighbors = []

    ### immediate/adjacent neighbors - 1 degree
    neighbors+= [getTemperature(Coordinate(p.X - 0.5, p.Y, p.Z),timestep)]
    neighbors+= [getTemperature(Coordinate(p.X + 0.5, p.Y, p.Z),timestep)]

    neighbors+= [getTemperature(Coordinate(p.X, p.Y - 0.5, p.Z),timestep)]
    neighbors+= [getTemperature(Coordinate(p.X, p.Y + 0.5, p.Z),timestep)]

    neighbors+= [getTemperature(Coordinate(p.X, p.Y, p.Z - 0.5),timestep)]
    neighbors+= [getTemperature(Coordinate(p.X, p.Y, p.Z + 0.5),timestep)]

    ### distance - 2 degree
    neighbors+= [getTemperature(Coordinate(p.X - 0.5, p.Y - 0.5, p.Z),timestep)]
    neighbors+= [getTemperature(Coordinate(p.X - 0.5, p.Y + 0.5, p.Z),timestep)]
    neighbors+= [getTemperature(Coordinate(p.X + 0.5, p.Y - 0.5, p.Z),timestep)]
    neighbors+= [getTemperature(Coordinate(p.X + 0.5, p.Y + 0.5, p.Z),timestep)]

    neighbors+= [getTemperature(Coordinate(p.X, p.Y - 0.5, p.Z - 0.5),timestep)]
    neighbors+= [getTemperature(Coordinate(p.X, p.Y + 0.5, p.Z - 0.5),timestep)]
    neighbors+= [getTemperature(Coordinate(p.X, p.Y - 0.5, p.Z + 0.5),timestep)]
    neighbors+= [getTemperature(Coordinate(p.X, p.Y + 0.5, p.Z + 0.5),timestep)]

    neighbors+= [getTemperature(Coordinate(p.X - 0.5, p.Y, p.Z - 0.5),timestep)]
    neighbors+= [getTemperature(Coordinate(p.X + 0.5, p.Y, p.Z - 0.5),timestep)]
    neighbors+= [getTemperature(Coordinate(p.X - 0.5, p.Y, p.Z + 0.5),timestep)]
    neighbors+= [getTemperature(Coordinate(p.X + 0.5, p.Y, p.Z + 0.5),timestep)]

    ### diagonal neighbors distance - 3 degree
    neighbors+= [getTemperature(Coordinate(p.X - 0.5, p.Y - 0.5, p.Z - 0.5),timestep)]
    neighbors+= [getTemperature(Coordinate(p.X - 0.5, p.Y + 0.5, p.Z - 0.5),timestep)]
    neighbors+= [getTemperature(Coordinate(p.X + 0.5, p.Y - 0.5, p.Z - 0.5),timestep)]
    neighbors+= [getTemperature(Coordinate(p.X + 0.5, p.Y + 0.5, p.Z - 0.5),timestep)]

    neighbors+= [getTemperature(Coordinate(p.X - 0.5, p.Y - 0.5, p.Z + 0.5),timestep)]
    neighbors+= [getTemperature(Coordinate(p.X - 0.5, p.Y + 0.5, p.Z + 0.5),timestep)]
    neighbors+= [getTemperature(Coordinate(p.X + 0.5, p.Y - 0.5, p.Z + 0.5),timestep)]
    neighbors+= [getTemperature(Coordinate(p.X + 0.5, p.Y + 0.5, p.Z + 0.5),timestep)]

    return neighbors
