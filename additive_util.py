import pandas as pd
import numpy as np
import warnings
import math
import time
import json
import os
from numpy import save,load

DEFAULT_TEMP = 300
# NON_EXISTING_TEMP = -99
NON_EXISTING_TEMP = 300

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
    return load(fullPath, allow_pickle=True)


def saveNumpy(obj, name, path='.'):
    """
    Saves numpy file
    """
    if ".npy" not in name:
        fullPath = path+'/'+name
        save(fullPath, obj, allow_pickle=True)
        print(name,'saved successfully in',path)
    else:
        fullPath = path+'/'+name.split(".npy")[0]
        save(fullPath, obj, allow_pickle=True)
        print(name,'saved successfully in',path)


def loadDict(name,path='.'):
    """
    Load dictionary of voxels
    """
    if ".dict" not in name:
        name += '.dict'

    if ".npy" in name:
        fullPath = path+'/'+name
    else:
        fullPath = path+'/'+name+'.npy'
    return load(fullPath).tolist()


def saveDict(obj, name, path='.'):
    """
    Save dictionary of voxels
    """
    if ".dict" not in name:
        fullPath = path+'/'+name+'.dict'
        save(fullPath, obj)
        print(name,'saved successfully in',path)
    else:
        fullPath = path+'/'+name
        save(fullPath, obj)
        print(name,'saved successfully in',path)