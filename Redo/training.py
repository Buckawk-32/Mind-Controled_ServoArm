import numpy as np 
import keras
import tensorflow as tf
from pandas.core.frame import DataFrame
from tensorflow.python.keras.utils.all_utils import to_categorical
from tensorflow.python.keras.optimizer_v1 import Adam
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Conv1D, MaxPooling1D, Flatten, Dense, Activation
from tensorflow.python.keras.callbacks import ModelCheckpoint
from keras.layers import BatchNormalization
import time
from Redo import HeadsetConnector
from sklearn.preprocessing import MinMaxScaler
from collections import deque
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)

n_samples = 30

dataNameList = ['attention','meditation','rawValue','delta','theta','lowAlpha','highAlpha',
            'lowBeta','highBeta','lowGamma','midGamma','poorSignal']
featureList = ['attention','meditation','rawValue','delta','theta','lowAlpha','highAlpha',
            'lowBeta','highBeta','lowGamma','midGamma']

ACTIONS = ["down", "none", "up"]

n_actions = len(ACTIONS)

trainDataDict = {}
for data in dataNameList:
    trainDataDict[data] = []
testDataDict = {}
for data in dataNameList:
    testDataDict[data] = []
valDataDict = {}
for data in dataNameList:
    valDataDict[data] = []

def load_data(dataDict, action, count):
    for data in featureList:
        dataDict[data].append(np.load("Python_Controlling/data/{}/{}/{}.npy".format(action, count, data), allow_pickle=True))

        # # Check if the loaded data is a dictionary
        # if isinstance(loaded_data, dict):
        #     raise ValueError(f"Loaded data for {data} is a dictionary, not numeric. The data type that tehy are is {type(data)}")

        # for value in loaded_data:
        #     print(type(value))

        # # Check if the loaded data contains numeric values
        # if not all(isinstance(value, (int, float)) for value in loaded_data):
        #     raise ValueError(f"Loaded data for {data} contains non-numeric values")

        # # Append the loaded data to the dictionary
        # dataDict[data].append(loaded_data)

test_n_samples = int(n_samples/2)
test_size = n_actions * int(n_samples)
train_n_samples = round(n_samples/2)
train_size = n_actions * round(n_samples/2)

nums = np.arange(n_samples)

trainNums = np.concatenate([nums[:5],nums[10:15],nums[20:25]])
np.random.shuffle(trainNums)

testNums = np.concatenate([nums[5:10], nums[15:20], nums[25:30]])
np.random.shuffle(testNums)

valNums = testNums[:int(len(testNums)/2)]
testNums = testNums[int(len(testNums)/2):]


for action in ACTIONS:
    for i in trainNums:
        load_data(trainDataDict, action, i)
        
for action in ACTIONS:
    for i in testNums:
        load_data(testDataDict, action, i)

for action in ACTIONS:
    for i in valNums:
        load_data(valDataDict, action, i)

print(trainDataDict)


for data in featureList:
    trainDataDict[data] = np.array(trainDataDict[data])
for data in dataNameList:
    testDataDict[data] = np.array(testDataDict[data])
for data in dataNameList:
    valDataDict[data] = np.array(valDataDict[data])


trainData = []
for data in featureList:
    trainData.append(trainDataDict[data])
trainData = np.array(trainData)
print("Training data, shape", trainData.shape)
print("Training data, number of dimesions", trainData.ndim)
print("Training data, type", trainData.dtype)

testData = []
for data in featureList:
    testData.append(testDataDict[data])
testData = np.array(testData)
print("Testing data, shape", testData.shape)
print("Testing data, number of dimesions", testData.ndim)
print("Testing data, type", testData.dtype)

valData = []
for data in featureList:
    valData.append(valDataDict[data])
valData = np.array(valData)
print("Validating data, shape", valData.shape)
print("Validating data, number of dimesions", valData.ndim)
print("Validating data, type", valData.dtype)

trainActions = []
for i in range(n_actions):
    trainActions.append(np.ones(int(n_samples/2))*i)
trainActions = np.concatenate(trainActions)
train_indexes = np.arange(len(trainActions))
np.random.shuffle(train_indexes)

testActions = []
for i in range(n_actions):
    testActions.append(np.ones(len(testNums))*i)
testActions = np.concatenate(testActions) 
test_indexes = np.arange(len(testActions)) 
np.random.shuffle(test_indexes)

valActions = []
for i in range(n_actions):
    valActions.append(np.ones(len(valNums))*i)
valActions = np.concatenate(valActions)
val_indexes = np.arange(len(valActions))
np.random.shuffle(val_indexes)

x_train = []
for X in trainData:
    x_train.append(X)

x_test = []
for X in testData:
    x_test.append(X)

x_val = []
for X in valData:
    x_val.append(X)

# y_train = []
# for y in trainActions:
#     y_train.append(y)

# y_test = []
# for y in testActions:
#     y_test.append(y)

# y_val = []
# for y in valActions:
#     y_val.append(y)

# x_train = trainData[train_indexes]
# x_val = valData[val_indexes]
# x_test = testData[test_indexes]

y_train = trainActions[train_indexes]
y_val = valActions[val_indexes]
y_test = testActions[test_indexes]

# print(type(x_train))
# x_train = DataFrame.astype(x_train, dtype="float32")
# print(type(x_train))

batch_size = 4
num_classes = n_actions
epochs = 50

img_rows, img_cols = 10, 10
channel = 11

# print("Data types and dimensions in x_train:")
# for data in dataNameList:
#     print(f"{data}: {type(trainDataDict[data][0])}")
#     print(f"{data} shape: {trainDataDict[data][0].shape}")

x_train = np.array(x_train).reshape(-1, 11, 1)
x_test = np.array(x_test).reshape(-1, 11, 1)
x_val = np.array(x_val).reshape(-1, 11, 1)

input_shape = (11, 1)

print('x_train shape:', x_train.shape)
print(x_train.shape[0], 'train samples')
print(x_test.shape[0], 'test samples')
print(x_val.shape[0], 'validation samples')

y_train = np.array(y_train)
y_test = np.array(y_test)
y_val = np.array(y_val)

y_train = to_categorical(y_train, num_classes=num_classes)
y_test = to_categorical(y_test, num_classes=num_classes)
y_val = to_categorical(y_val, num_classes=num_classes)

tf.compat.v1.disable_eager_execution()

model = Sequential()
model.add(Conv1D(64, (3), input_shape=input_shape))
model.add(Activation('relu'))

model.add(Conv1D(64, (2)))
model.add(Activation('relu'))
model.add(MaxPooling1D(pool_size=(2)))

model.add(Flatten())

model.add(Dense(512))

model.add(Dense(3))
model.add(Activation('softmax'))

checkp = ModelCheckpoint('models/cnn_model.hdf5', monitor="val_loss", save_best_only=True)

model.compile(loss='categorical_crossentropy',
              optimizer=Adam(),
              metrics=['accuracy'])

for epoch in range(epochs):
    model.fit(x_train, y_train,
          batch_size=batch_size,
          epochs=epochs,
          verbose=1,
          validation_data=(x_val, y_val),
          callbacks=[checkp])
    
    score = model.evaluate(x_test, y_test, batch_size=batch_size)

    MODEL_NAME = f"/new_models/{round(score[1]*100,2)}-acc-64x3-batch-norm-{epoch}epoch-{int(time.time())}-loss-{round(score[0],2)}.model"
    model.save(MODEL_NAME)

print("saved: ")
print(MODEL_NAME)

