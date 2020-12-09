"""
This file contains all tuning parameter needed in the process
"""
# ----------------------------------------------------------
# 1. Feature Selection
# ----------------------------------------------------------
# Size of the images (The image must be in square shaped)
IMG_HEIGHT = 300
IMG_WIDTH = 300

# Turn image into black and white
BW_THRES = 90

# Erotion and dilation transformation
APPLY_ERO_AND_DIL = False
ERO_DIL_KERNEL_SIZE = (2, 2) # Default is (2, 2)
ERO_AND_DIL_ITERATION = 1

# Remove massive black parameter
MASSIVE_FILTER_SIZE = 15 # Must be an odd number (It is recommended to have this value divide IMG_WIDTH and IMG_HEIGHT)
MIN_BLACK = 135 # Not greater than MASSIVE_FILTER_SIZE
FILTER_STEP = 3 # The default value is the same as MASSIVE_FILTER_SIZE

# Remove noise
REMOVE_NOISE = False # Set to true if you want to include noise removal process
NOISE_FILTER_SIZE = 5 # Must be an odd number (It is recommended to have this value divide IMG_WIDTH and IMG_HEIGHT)
MAX_BLACK = 1 # Not greater than the square of MASSIVE_FILTER_SIZE
NOISE_FILTER_STEP = 5 # The default value is the same as MASSIVE_FILTER_SIZE

# DFS related
DFS_RADIUS = 3
FEATURE_THRES = 15
BOR_BOUND = 8
ROI_HOR_TOP_THRES = 290
ROI_HOR_BOTTOM_THRES = 200
ROI_VER_TOP_THRES = 297
ROI_VER_BOTTOM_THRES = 200

# Draw border of each feature and crop them as new image
DISPLAY_BORDERED_FEATURES = False
BORDER_PADDING = 0
ADD_PADDING = 0

# Save the feature images into a folder
SAVE_FEATURES = False

# Shape of feature images which will be fed into the model
MODEL_HEIGHT = 35
MODEL_WIDTH = 35

# ----------------------------------------------------------
# 2. Build and Train Model
# ----------------------------------------------------------
# If you want to use your own model, place it in model folder
MODEL_ARCHITECTURE = 'cnn_model_1.tflite'

# Some parameters related to model training process
SAVE_TO = 'core/model/cnn_model_2.hdf5'
BATCH_SIZE = 32
EPOCHS = 5

# Set to true if you want to display predicted features from model in terminal
DISPLAY_PREDICTED_FEATURES = True

# ----------------------------------------------------------
# 3. Display Question and Answer
# ----------------------------------------------------------
# Turn to true if you want to display the question and answer in the terminal
DISPLAY_QNA = True

# ----------------------------------------------------------
# 4. General
# ----------------------------------------------------------
# Set to true if you want to delete processed image saved in firebase
DELETE_PROCESSED_IMAGE = False
