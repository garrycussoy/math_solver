"""
This file is designed to train model using simple NN
"""

# Import some packages needed
from tensorflow import keras
from tensorflow.keras.optimizers import RMSprop
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import tensorflow as tf
import numpy as np
import pandas as pd
import cv2
import os

# Import some parameters from other file
from parameter import MODEL_HEIGHT
from parameter import MODEL_WIDTH
from parameter import SAVE_TO
from parameter import BATCH_SIZE
from parameter import EPOCHS

# Define directories
train_dir = "/Users/garry/Math_Solver/train_set/"

"""
------------------------------------------------------------------
Create Generator
------------------------------------------------------------------
"""
# Create Image Data Generator
train_datagen = ImageDataGenerator(rescale = 1.0 / 255.)

# Create train geneator
train_generator = train_datagen.flow_from_directory(
  train_dir,
  batch_size = 32,
  class_mode = 'categorical',
  target_size = (MODEL_HEIGHT, MODEL_WIDTH),
  color_mode = 'grayscale'
)

"""
------------------------------------------------------------------
Build and Train NN Model
------------------------------------------------------------------
"""
# Build the model
model = tf.keras.models.Sequential([
  # Convolution layer
  tf.keras.layers.Conv2D(128, (3, 3), activation = 'relu', input_shape = (MODEL_HEIGHT, MODEL_WIDTH, 1)),
  tf.keras.layers.MaxPooling2D(pool_size = 2, strides = 2),

  # Fully connected layer
  tf.keras.layers.Flatten(),
  tf.keras.layers.Dense(512, activation = 'relu'), 
  tf.keras.layers.Dense(15, activation = 'softmax')  
])

# Define checkpoint
model_checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(
  filepath = SAVE_TO,
  monitor = 'loss',
  mode = 'min',
  save_best_only = True,
  verbose = 1
)

# Compile the models
model.compile(
  optimizer = RMSprop(lr = 0.001),
  loss = 'categorical_crossentropy',
  metrics = ['accuracy']
)

# Train the model
model.fit(
  train_generator,
  batch_size = BATCH_SIZE,
  epochs = EPOCHS,
  verbose = 1,
  callbacks = [model_checkpoint_callback]
)
