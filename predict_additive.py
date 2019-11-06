import pandas as pd
import numpy as np
import os
from time import time
from additive_util import loadNumpy
from sklearn.linear_model import LinearRegression,Ridge


historicalColumns,neighborColumns = [],[]

for historical in range(5):
    historicalColumns += ['Tminus'+str(historical+1)]

for neighbor in range(26):
    neighborColumns += ['T'+str(neighbor+1)+'_t-1']

columns = ['timestep','x_voxel','y_voxel','z_voxel','layerNum','time_creation','x_laser','y_laser','z_laser','x_distance','y_distance','z_distance','euclidean_distance_laser'] + historicalColumns+ neighborColumns+['T_self']


def combineDataFrames(prefix,columns=columns):
    List = []
    nums_start,nums_stop = [],[]
    for item in os.listdir(prefix):
        if "data_" in item and ".npy" in item:
            timeStep_start = int(item.split(prefix+'_')[1].split('_')[0])
            nums_start += [timeStep_start]

            timeStep_stop = int(item.split('_')[3].split('.npy')[0])
            nums_stop += [timeStep_stop]

    nums_start = sorted(nums_start)
    nums_stop = sorted(nums_stop)

    array = loadNumpy(prefix+'/'+prefix+'_'+str(nums_start[0])+'_'+str(nums_stop[0])+'.npy')
    for i in range(1,len(nums_start)):
        newFile = prefix+'/'+prefix+'_'+str(nums_start[i])+'_'+str(nums_stop[i])+'.npy'
        array = np.append(array,loadNumpy(newFile),axis=0)
    return pd.DataFrame(array,columns=columns)

df = combineDataFrames('data_big')
df_mini = df[df['timestep'] < 500.0]

df_mini.to_csv('data_500_timesteps.csv',index=False)
print 'Saved'

df_train = df_mini[df_mini['timestep'] < 400.0]
df_test = df_mini[df_mini['timestep'] >= 400.0]
featureColumns = ['timestep','x_distance','y_distance','z_distance','time_creation','Tminus1']+neighborColumns

X_train = df_train.loc[:,featureColumns ]
y_train = df_train['T_self']

X_test = df_test.loc[:,featureColumns ]
y_test = df_test['T_self']

start = time.time()
linear = LinearRegression()
linear.fit(X_train,y_train)
predicted = linear.predict(X_test)
stop = time.time()
stop = 5
start = 2
print 'The prediction took %2f ', (stop -start),'seconds'
print r2(y_test,predicted) ,mape(y_test,predicted)
