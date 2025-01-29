import numpy as np

import tensorflow as tf
from tensorflow.python.keras.utils.all_utils import to_categorical
from tensorflow.python.keras.optimizer_v1 import Adam
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Conv1D, MaxPooling1D, Flatten, Dense, Activation
from tensorflow.python.keras.callbacks import ModelCheckpoint

import time