from utility import *
from sys import argv
warnings.filterwarnings('ignore')

###The dataframes are getting loaded from the csv file
print 'Printing new create data ....'

DEFAULT_TEMP = 300
NON_EXISTING_TEMP = -99

def createDatabase(dataframe,timestep_Start,timestep_Stop):
    """
    It transforms the data into a database for each voxel at each time step
    """
    start = time.time()
    neighborColumns,historicalColumns,dictList = [],[],[]

    ## The temperature at this point for the past few timesteps
    for historical in range(5):
        historicalColumns += ['Tminus'+str(historical+1)]

    ## The temperature of neighboring 26 voxel elements
    for neighbor in range(26):
        neighborColumns += ['T'+str(neighbor+1)+'_t-1']

    columns = ['voxelLat','voxelLong','voxelVert','timestep','x_voxel','y_voxel','z_voxel','layerNum','time_creation','x_laser','y_laser','z_laser','x_distance','y_distance','z_distance','euclidean_distance_laser'] + historicalColumns+ neighborColumns+['T_self']

    num_timesteps = len(dataframe.loc[0]-4)
    num_voxels = len(dataframe)

    for timestep in range(timestep_Start,timestep_Stop):#range(1,num_timesteps+1):
        for voxel in indices.keys():
            x,y,z = voxel

            voxelPosObject = Coordinate(x,y,z)
            T_self = getTemperature(voxelPosObject,timestep)
            if T_self == DEFAULT_TEMP:
                continue

            ##Extract the position of the laser
            x_laser,y_laser,z_laser = tuple(toolpath[timestep-1])

            ##Extract the absolute distance between the laser position and voxil position
            x_distance, y_distance, z_distance = abs(x-x_laser), abs(y-y_laser),abs(z-z_laser)

            ##Each layer is 0.5 so we can find number of layer by dividing height by 0.5
            layerNum = z/0.5

            laserPosObject = Coordinate(x_laser,y_laser,z_laser)

            distance_laser = voxelPosObject.distance(laserPosObject)

            dfIndex = indices[voxel]
            row = dataframe.loc[dfIndex].tolist()
            time_creation = float(row[3])
            time_current = float(timestep*0.1)
            time_elapsed = time_current - time_creation

            dictionary = {'voxelLat':'interior','voxelLong':'interior','voxelVert':'interior',
                        'timestep':timestep,
                        'x_voxel':x, 'y_voxel':y, 'z_voxel':z, 'layerNum':layerNum,
                         'time_creation':time_creation, 'x_laser':x_laser,'y_laser':y_laser,'z_laser':z_laser,
                         'x_distance':x_distance,'y_distance':y_distance,'z_distance':z_distance,
                          'distance_laser':distance_laser}

            ##Extract the temperature of a voxel based on position and timestep
            for i in range(5):
                dictionary[historicalColumns[i]] = getTemperature(voxelPosObject,timestep-i-1)

            ##Extract the temperature of the neighboring temperatures
            neighborTemps = findNeighborTemperatures(voxelPosObject,timestep)
            for i in range(len(neighborTemps)):
                key = 'T'+str(i+1)+'_t-1'
                if neighborTemps[i] == DEFAULT_TEMP:
                    dictionary[key] = NON_EXISTING_TEMP
                    if i==0 or i==1:
                        dictionary['voxelLat'] = 'missing'
                    if i==3 or i==2:
                        dictionary['voxelLong'] = 'missing'
                    if i==5:
                        dictionary['voxelVert'] = 'missing'

                else:
                    dictionary[key] = neighborTemps[i]

            if dictionary['voxelVert'] == 'interior' and dictionary['voxelLong'] == 'interior' and dictionary['voxelLat'] == 'interior':
                dictionary['voxelType'] = 'interior'



            dictionary['T_self'] = T_self

            dictList += [dictionary]

    database =  pd.DataFrame(dictList,columns=columns)
    stop = time.time()
    print 'Database creation took',stop-start,'seconds'

    return database

if __name__ == "__main__":
    import argparse as ap
    args = argparse.ArgumentParser()

    parser.add_argument("-d", "--directory", help = "directory & name of input csv file", required=True)
    parser.add_argument("-i", "--indices", help = "filename of index dictionary", required=True)
    parser.add_argument("-s", "--start", help= "Timestep for starting data creation", required=True)
    parser.add_argument("-e", "--end", help= "Timestep for stopping data creation", required=True)

    directory = args["directory"]
    index_file = args["indices"]
    timestep_start = args["start"]
    timestep_end = args["end"]


    indices = loadDict(index_file)
    toolpath, state, endTime = parse_toolpath(directory,'toolpath.crs',0.1)

    df = pd.read_csv(directory +'/'+directory+'.csv',header=None)
    db = createDatabase(df,timestep_start,timestep_end)
    saveNumpy(db,directory+'_'+str(timestep_start)+'_'+str(timestep_end))
