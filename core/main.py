"""
This file contains the main process.
1. Feature selection
2. Feed feature into model
3. Turn features into mathematical terms
4. Evaluate the problem
"""

# Import some packages needed
from tensorflow.keras.models import load_model
import numpy as np
import cv2
import argparse

# Import functions from other files
from core.feature_extraction import reshape_square
from core.feature_extraction import black_or_white
from core.feature_extraction import remove_massive_black
from core.feature_extraction import remove_noise
from core.feature_extraction import sharpen
from core.feature_extraction import is_pos
from core.feature_extraction import get_features
from core.feature_extraction import draw_border
from core.feature_extraction import get_features_as_img
from core.math_terms import arrange_position
from core.math_terms import get_math_terms
from core.evaluate import evaluate
from core.display import display_qna

# Import variables from other files
from core.math_symbol import math_symbol

# Import some tuning parameters
from core.parameter import IMG_HEIGHT
from core.parameter import IMG_WIDTH
from core.parameter import BW_THRES
from core.parameter import APPLY_ERO_AND_DIL
from core.parameter import ERO_DIL_KERNEL_SIZE
from core.parameter import ERO_AND_DIL_ITERATION
from core.parameter import MASSIVE_FILTER_SIZE 
from core.parameter import MIN_BLACK
from core.parameter import FILTER_STEP
from core.parameter import REMOVE_NOISE
from core.parameter import NOISE_FILTER_SIZE
from core.parameter import MAX_BLACK
from core.parameter import NOISE_FILTER_STEP
from core.parameter import DFS_RADIUS
from core.parameter import DISPLAY_BORDERED_FEATURES
from core.parameter import BORDER_PADDING
from core.parameter import FEATURE_THRES
from core.parameter import BOR_BOUND
from core.parameter import MODEL_HEIGHT
from core.parameter import MODEL_WIDTH
from core.parameter import ADD_PADDING
from core.parameter import MODEL_ARCHITECTURE
from core.parameter import DISPLAY_PREDICTED_FEATURES
from core.parameter import DISPLAY_QNA

"""
Following function is the main function to get the problem image, process it, and generate the solution.

:param numpy-array image: The problem image that will be processed
:param string topic: Topic of the problem
"""
def solve(image, topic):
  """
  ------------------------------------------------------------
  STEP 1. Feature Selection
  1. Do some preprocessing to the image
  2. Turn the image into black and white
  3. Apply erotion and dilation (optional)
  3. Remove massive black
  4. Remove noise (optional)
  5. Get all features information
  6. Crop the features as collection of images to be feed into the model
  ------------------------------------------------------------
  """
  # Reshape the image into square-shaped
  image = reshape_square(image)

  # Do some preprocessing
  image = cv2.resize(image, (IMG_HEIGHT, IMG_WIDTH)) # Resize the image
  ori_reshape = np.copy(image) # Copy original reshaped image
  image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # Turn to grayscale

  # Turn the image into just black and white pixels
  image = black_or_white(image)

  # Apply erotion and dilation
  if APPLY_ERO_AND_DIL:
    # Define kernel
    kernel = np.ones(ERO_DIL_KERNEL_SIZE, np.uint8)

    # Apply erotion and dilation
    image = cv2.erode(image, kernel, iterations = ERO_AND_DIL_ITERATION)
    image = cv2.dilate(image, kernel, iterations = ERO_AND_DIL_ITERATION)

  # Remove massive black pixels
  image = remove_massive_black(image, MASSIVE_FILTER_SIZE, FILTER_STEP, MIN_BLACK)

  # Remove noise
  if REMOVE_NOISE:
    image = remove_noise(image, NOISE_FILTER_SIZE, NOISE_FILTER_STEP, MAX_BLACK)

  # Get all features information from the image
  features = get_features(image)

  # Draw border into each features in the original reshaped image
  if DISPLAY_BORDERED_FEATURES:
    # Draw all features border
    for feature in features:
      ori_reshape = draw_border(ori_reshape, feature)

    # Show bordered features
    cv2.imshow("Bordered Features Image", ori_reshape)
    cv2.waitKey(0)

  # Get all features as an image
  feature_col = get_features_as_img(image, features)
  feature_col = np.array(feature_col)

  """
  ------------------------------------------------------------
  STEP 2. Predict the Feature
  1. Feed feature image to the model
  2. Get predicted value for each feature
  ------------------------------------------------------------
  """
  # Load the model
  model = load_model("core/model/" + MODEL_ARCHITECTURE)

  # Predict the feature
  feature_col = feature_col.reshape(feature_col.shape + (1,)) 
  features_prob = model.predict(feature_col)
  features_pred = []
  for index in range(len(feature_col)):
    predicted_feat = np.argmax(features_prob[index])
    features_pred.append(predicted_feat)

  # Assign the predicted value to each component
  for index in range(len(features)):
    features[index]["symbol_id"] = features_pred[index]
    features[index]["symbol"] = math_symbol[features_pred[index]]["symbol"]

  # Display predicted features from model in terminal
  if DISPLAY_PREDICTED_FEATURES:
    print("--------------------------------------------------------------")
    print("Predicted Features :")
    print(features_pred)
    print("--------------------------------------------------------------")

  """
  ------------------------------------------------------------
  STEP 3. Turn Features Into Mathematical Terms
  1. Get the position order of each features
  2. Turn those features into mathematical terms
  ------------------------------------------------------------
  """
  # Get position order for each feature
  features = arrange_position(features)

  # Turn features into mathematical terms
  terms = get_math_terms(features, topic)
  display_terms = terms.copy()

  """
  ------------------------------------------------------------
  STEP 4. Evaluate the Problem
  ------------------------------------------------------------
  """
  # Choose the topic and evaluate the problem
  result = evaluate(terms, topic)

  """
  ------------------------------------------------------------
  OPTIONAL. Display the Question and Answer in Terminal
  ------------------------------------------------------------
  """
  if DISPLAY_QNA:
    # Display the question and answer in terminal
    display_qna(display_terms, result, topic)
