import os, sys 
import numpy as np 
import tensorflow as tf 
from tensorflow import keras
import tensorflow_datasets as tfds
import matplotlib.pyplot as plt 
from keras import layers, models
import keras

DIR = "Intersteller Objects"

TRAIN_DIR = keras.utils.image_dataset_from_directory(
    DIR,
    validation_split=0.2,
    subset="training",
    shuffle=True,
    seed=110,
    image_size=(512,512)
)
