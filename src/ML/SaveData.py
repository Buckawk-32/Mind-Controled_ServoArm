import numpy as np
import time
from collections import deque
import os

from Redo import HeadsetConnector


# * All of the constants

FEATURES = ['attention','meditation','rawValue','delta','theta','lowAlpha','highAlpha',
            'lowBeta','highBeta','lowGamma','midGamma']

LABELS = ["up", "down", "none"]
DATASET = "Python_Controlling/data"

headset = HeadsetConnector.NeuroPy(port="COM3")

# * Checking whether the dataset directory exists

if not os.path.exists(DATASET):
    os.mkdir(DATASET)

print(LABELS)
lable = input("Lable/Action: ")

action_dataset = f"{DATASET}/{lable}" 
if not os.path.exists(action_dataset):
    os.mkdir(action_dataset)


def save(headset_data, action, count):
    print(f"Saving {lable} data...")
    for data in FEATURES:
        np.save(os.path.join(DATASET, "{}/{}/{}.npy".format(action, count, data)), np.array(headset_data))

    print("Finished Saving Data")

def load(DataArray, action, count):
    for data in FEATURES:
        # TODO: see whether the [:100] is needed
        DataArray[data].append(np.load(os.path.join(DATASET, "{}/{}/{}.npy".format(action, count, data)), allow_pickle=True)[:100])

def readHeadsetData():
    for data in FEATURES:
        dict[data].

dict = dict