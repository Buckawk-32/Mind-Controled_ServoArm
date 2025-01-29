from pylsl import StreamInlet, resolve_stream
import numpy as np 
import time
import matplotlib.pyplot as plt
from matplotlib import style
from collections import deque
import cv2
import os
import random
import tensorflow.python.keras as tf
from Redo import HeadsetConnector
from sklearn.preprocessing import MinMaxScaler

np.random.seed(42)

dataNameList = ['attention','meditation','rawValue','delta','theta','lowAlpha','highAlpha',
            'lowBeta','highBeta','lowGamma','midGamma','poorSignal']

dataNameList = ['attention','meditation','rawValue','delta','theta','lowAlpha','highAlpha',
            'lowBeta','highBeta','lowGamma','midGamma','poorSignal']
featureList = ['attention','meditation','rawValue','delta','theta','lowAlpha','highAlpha',
            'lowBeta','highBeta','lowGamma','midGamma']

ACTIONS = ["up", "down", "none"]

ACTION = "down"


MODEL_NAME = ""

HM_SECS = 10
TOTAL_ITERS = HM_SECS*1
BOX_MOVE = "model"

WIDTH = 800
HEIGHT = 800
SQ_SIZE = 50
MOVE_SPEED = 1

square = {"x1": int(int(WIDTH)/2-int(SQ_SIZE/2)),
          "x2": int(int(WIDTH)/2+int(SQ_SIZE/2)),
          "y1": int(int(HEIGHT)/2-int(SQ_SIZE/2)),
          "y2": int(int(HEIGHT)/2+int(SQ_SIZE/2))}

n_label = len(ACTIONS)

total = 0
up = 0
down = 0
none = 0
correct = 0

trainDataDict = dict()
for data in dataNameList:
    trainDataDict[data] = []


datadir = "Python_Controlling/data"
if not os.path.exists(datadir):
    os.mkdir(datadir)

actiondir = f"{datadir}/{ACTION}"
if not os.path.exists(actiondir):
    os.mkdir(actiondir)
        
def save_data(headset, action, count):
    print(f"saving {ACTION} data...")
    for data in featureList:
        np.save(os.path.join(datadir, "{}/{}/{}.npy".format(action, count, data)), np.array(headset))
    print("done.")

def load_model():
    loaded_model = tf.models.load_model(MODEL_NAME)

def load_data(dataDict, action, count):
    for data in featureList:
        dataDict[data].append(np.load("Python_Controlling/data/{}/{}/{}.npy".format(action, count, data), allow_pickle=True)[:100])


n_samples = 30
test_n_samples = int(n_samples/2)
test_size = n_label * int(n_samples/2)
train_n_samples = round(n_samples/2)
train_size = n_label * round(n_samples/2)

nums = np.arange(n_samples)
trainNums = np.concatenate([nums[:30]])

np.random.shuffle(trainNums)

def init_DataDict():
    for data in dataNameList:
        data_dict[data] = deque(maxlen=1000)
        
def predict(model, values):
    values = scaler.transform(values.reshape(-1, 1100))
    preds = int(np.array(model.predict(values))[0])
    print('\npreds : ', preds)
    return preds

def read_data():
    for data in featureList:
        data_dict[data].append(getattr(headset, data))
        print(f"{data}:", getattr(headset, data))

headset = HeadsetConnector.NeuroPy("COM3")
headset.start()

time.sleep(10)

data_dict = dict()

init_DataDict()


for i in trainNums:
    read_data()
    path = f"{datadir}/{ACTION}/{i}"
    os.mkdir(path)
    time.sleep(2)
    save_data(data_dict, ACTION, i)

for action in ACTIONS:
    for i in trainNums:
        load_data(trainDataDict, action, i)

for data in dataNameList:
    trainDataDict[data] = np.array(trainDataDict[data])

trainData = []
for data in featureList:
    trainData.append(trainDataDict[data])
trainData = np.array(trainData).transpose(1, 0, 2)

trainActions = []
for i in range(n_label):
    trainActions.append(np.ones(int(n_samples/2))*i)
trainActions = np.concatenate(trainActions)
train_indexes = np.arange(len(trainActions))
np.random.shuffle(train_indexes)

x_train = trainData[train_indexes]

img_rows, img_cols = 10, 10
channel = 11

print(x_train)

x_train = x_train.astype('float32')
scaler = MinMaxScaler()
print(scaler.fit(x_train.reshape(-1, 1100)))






box = np.ones((square['y2']-square['y1'], square['x2']-square['x1'], 3)) * np.random.uniform(size=(3,))
horizontal_line = np.ones((HEIGHT, 10, 3)) * np.random.uniform(size=(3,))
vertical_line = np.ones((10, WIDTH, 3)) * np.random.uniform(size=(3,))



