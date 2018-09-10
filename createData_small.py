from utility import *
from sys import argv
warnings.filterwarnings('ignore')

###The dataframes are getting loaded from the csv file
print 'Printing new create data ....'
indices = loadDict('indices_big')
toolpath, state, endTime = parse_toolpath('20-20-10-800/','toolpath.crs',0.1)
DEFAULT_TEMP = 300
NON_EXISTING_TEMP = -99

def createDatabase(dataframe,timestep_Start,timestep_Stop):
    start = time.time()
    neighborColumns,historicalColumns,dictList = [],[],[]

    for historical in range(5):
        historicalColumns += ['Tminus'+str(historical+1)]

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

            x_laser,y_laser,z_laser = tuple(toolpath[timestep-1])
            x_distance, y_distance, z_distance = abs(x-x_laser), abs(y-y_laser),abs(z-z_laser)
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


            for i in range(5):
                dictionary[historicalColumns[i]] = getTemperature(voxelPosObject,timestep-i-1)


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

def main():
    directory = str(argv[1])
    df = pd.read_csv(directory +'/'+directory+'.csv',header=None)
    timestep_Start,timestep_Stop = int(argv[2]), int(argv[3])
    db = createDatabase(df,timestep_Start,timestep_Stop)
    saveNumpy(db,'data_smallerSim_'+str(timestep_Start)+'_'+str(timestep_Stop))

if __name__ == "__main__":
    main()
