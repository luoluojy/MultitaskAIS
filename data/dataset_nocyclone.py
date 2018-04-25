#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 20 09:50:23 2018

@author: vnguye04
"""

import numpy as np
import matplotlib.pyplot as plt
import pickle

LAT, LON, SOG, COG, HEADING, ROT, NAV_STT, TIMESTAMP, MMSI = range(9)

## Training set no cyclone
###############################################################################

with open("/homes/vnguye04/Bureau/Sanssauvegarde/Datasets/MarineC/dataset5/dataset5_train.pkl","rb") as f:
    Vs_train = pickle.load(f)

Vs = Vs_train
for key in Vs.keys():
    tmp = Vs[key]
    plt.plot(tmp[:,1],tmp[:,0])
plt.xlim([0,1])
plt.ylim([0,1])

for key in Vs.keys():
    tmp = Vs[key]
    lat_max = np.max(tmp[:,LAT])
    lon_max = np.max(tmp[:,LON])
    lat_min = np.min(tmp[:,LAT])
    lon_min = np.min(tmp[:,LON])
    if (lat_max < 0.24) and (lat_min > 0.155) and (lon_max<0.53) and (lon_min>0.485):
        Vs.pop(key,None)
    
with open("/homes/vnguye04/Bureau/Sanssauvegarde/Datasets/MarineC/dataset5/dataset5_train_nocyclone.pkl","wb") as f:
    pickle.dump(Vs,f)
    
## Test set moved cyclone
###############################################################################

with open("/homes/vnguye04/Bureau/Sanssauvegarde/Datasets/MarineC/dataset3/dataset3_test.pkl","rb") as f:
    Vs_test = pickle.load(f)

# For dataset4_movedcyclone: because there are no cyclones whose duration > 12h in the dataset4_test, we
# used cyclones in the dataset4_train 

Vs = Vs_test
for key in Vs.keys():
    tmp = Vs[key]
    lat_max = np.max(tmp[:,LAT])
    lon_max = np.max(tmp[:,LON])
    lat_min = np.min(tmp[:,LAT])
    lon_min = np.min(tmp[:,LON])
    if (lat_max < 0.24) and (lat_min > 0.155) and (lon_max<0.53) and (lon_min>0.485):
        print("key: ", key, "mmsi: ", tmp[0,MMSI])
        Vs[key][:,LON] += 2/10.5
        Vs[key][:,LAT] += 1.55/3.5
    else:
        Vs.pop(key,None)

with open("/homes/vnguye04/Bureau/Sanssauvegarde/Datasets/MarineC/dataset3/dataset3_test_movedcyclones.pkl","wb") as f:
    pickle.dump(Vs,f)


## Test set only cyclone
###############################################################################

with open("/homes/vnguye04/Bureau/Sanssauvegarde/Datasets/MarineC/dataset3/dataset3_test.pkl","rb") as f:
    Vs_test = pickle.load(f)

# For dataset4_movedcyclone: because there are no cyclones whose duration > 12h in the dataset4_test, we
# used cyclones in the dataset4_train 

Vs = Vs_test
for key in Vs.keys():
    tmp = Vs[key]
    lat_max = np.max(tmp[:,LAT])
    lon_max = np.max(tmp[:,LON])
    lat_min = np.min(tmp[:,LAT])
    lon_min = np.min(tmp[:,LON])
    if (lat_max < 0.24) and (lat_min > 0.155) and (lon_max<0.53) and (lon_min>0.485):
        print("key: ", key, "mmsi: ", tmp[0,MMSI])
    else:
        Vs.pop(key,None)

with open("/homes/vnguye04/Bureau/Sanssauvegarde/Datasets/MarineC/dataset3/dataset3_test_cyclones.pkl","wb") as f:
    pickle.dump(Vs,f)

# Step 10: Route Divergence
###############################################################################
with open("/homes/vnguye04/Bureau/Sanssauvegarde/Datasets/MarineC/dataset5/dataset5_test.pkl","rb") as f:
    Vs_test = pickle.load(f)

Vs = Vs_test

#for key in Vs.keys():
#    tmp = Vs[key]
#    lat_begin = tmp[0,LAT]
#    lat_end = tmp[-1,LAT]
#    lon_begin = tmp[0,LON]
#    lon_end = tmp[-1,LON]
#    if (lat_begin < 0.38) and (lat_begin > 0.35) and (lon_begin <0.43) and (lon_begin >0.36):
#        print("key: ", key, "mmsi: ", tmp[0,MMSI])
#    elif (lat_end < 0.38) and (lat_end > 0.35) and (lon_end <0.43) and (lon_end >0.36):
#        print("key: ", key, "mmsi: ", tmp[0,MMSI])        
#    else:
#        Vs.pop(key,None)
        
#for key in Vs.keys():
#    tmp = Vs[key]
#    print(tmp[0,MMSI], len(tmp)/2)
#    plt.figure()
#    plt.plot(tmp[:,1],tmp[:,0])
#    plt.title(str(tmp[0,MMSI]))
#    plt.xlim([0,1])
#    plt.ylim([0,1])


for key in Vs.keys():
    tmp = Vs[key]
    lat_begin = tmp[0,LAT]
    lat_end = tmp[-1,LAT]
    lon_begin = tmp[0,LON]
    lon_end = tmp[-1,LON]
    if (lat_end < 0.38) and (lat_end > 0.35) and (lon_end <0.43) and (lon_end >0.36):
        if int(tmp[0,MMSI]) == 368040076:
            plt.plot(tmp[:,1],tmp[:,0],color='g',linewidth=2)
            v_true = np.copy(tmp)    
    else:
        plt.plot(tmp[:,1],tmp[:,0],color='b')
plt.xlim([0,1])
plt.ylim([0,1])

Vs_divergence = dict()
for e in range(-3,1):
    Vs_divergence[e] = np.copy(v_true)
    Vs_divergence[e][:,LAT] += e*0.01
    
    
for key in Vs_divergence.keys():
    tmp = Vs_divergence[key]
    plt.plot(tmp[:,1],tmp[:,0],linewidth=2)

with open("/homes/vnguye04/Bureau/Sanssauvegarde/Datasets/MarineC/dataset3/dataset3_test_divergences.pkl","wb") as f:
    pickle.dump(Vs_divergence,f)

Vs_turns = dict()    
v_turn = np.zeros(175)
v_turn[115:] = np.arange(60)
for e in range(0,5):
    Vs_turns[e] = np.copy(v_true)
    Vs_turns[e][:,LAT] += (e)*0.0001*v_turn
for key in Vs_turns.keys():
    tmp = Vs_turns[key]
    plt.plot(tmp[:,1],tmp[:,0],linewidth=2)
with open("/homes/vnguye04/Bureau/Sanssauvegarde/Datasets/MarineC/dataset3/dataset3_test_turns.pkl","wb") as f:
    pickle.dump(Vs_turns,f)