"""
This file contains functions needed to extract features from an image.
"""
# Import some packages needed
import numpy as np
import cv2

# Import some tuning parameters
from core.parameter import IMG_HEIGHT
from core.parameter import IMG_WIDTH
from core.parameter import BW_THRES
from core.parameter import MASSIVE_FILTER_SIZE 
from core.parameter import MIN_BLACK
from core.parameter import FILTER_STEP
from core.parameter import REMOVE_NOISE
from core.parameter import NOISE_FILTER_SIZE
from core.parameter import MAX_BLACK
from core.parameter import NOISE_FILTER_STEP
from core.parameter import DFS_RADIUS
from core.parameter import BORDER_PADDING
from core.parameter import FEATURE_THRES
from core.parameter import BOR_BOUND
from core.parameter import MODEL_HEIGHT
from core.parameter import MODEL_WIDTH
from core.parameter import ADD_PADDING

"""
This function is designed to make the reshape the image into square one

:param numpy-array image: The image that will be reshaped
:return image: Reshaped image
"""
def reshape_square(image):
  # Set some variables
  sq_top = 0
  sq_left = 0
  sq_right = 0
  sq_bottom = 0

  # Get the size of the image
  image_shape = image.shape
  img_height = image_shape[0]
  img_width = image_shape[1]
  diff = img_width - img_height

  # Case when width < height
  if diff < 0:
    sq_left = (- diff) // 2
    sq_right = (- diff) // 2

  # Case when width > height
  elif diff > 0:
    sq_top = diff // 2
    sq_bottom = diff // 2

  # Add padding to the feature and resize it
  image = cv2.copyMakeBorder(
    image,
    sq_top,
    sq_bottom,
    sq_left,
    sq_right,
    cv2.BORDER_CONSTANT,
    value = (0, 0, 0)
  )

  # Return the black and white image
  return image

"""
This function is designed to make the images only black (0) or white (255)

:param numpy-array img: The image that want to be converted into black and white
:return img: Black and white image
"""
def black_or_white(img):
  # Loop through each pixel
  for row in range(IMG_HEIGHT):
    for col in range(IMG_WIDTH):
      # Turn into black
      if img[row, col] <= BW_THRES:
        img[row, col] = 0
      
      # Turn into white
      else:
        img[row, col] = 255
  
  # Return the black and white image
  return img

"""
This function is designed to remove massive black pixels and turn those into white pixels

:param numpy-array img: The image which will be modified
:param integer noise_filsize: The size of the filter
:param integer filstep: How long will the filter move horizontally in each step
:param integer minblack: Minimum number of black pixels in a filter which trigger removal process
:return new_img: Cleaner image without massive black pixels
"""
def remove_massive_black(img, noise_filsize, filstep, minblack):
  # Calculate some border point
  mid_point = (noise_filsize + 1) // 2
  left_most = mid_point - 1
  up_most = mid_point - 1
  right_most = IMG_WIDTH - mid_point + 1
  bottom_most = IMG_HEIGHT - mid_point + 1

  # Copy image
  new_img = np.copy(img)

  # Loop through each pixel
  for row in range(up_most, bottom_most + 1, filstep):
    for col in range(left_most, right_most + 1, filstep):
      # Loop for each pixel in noise filter square
      black_pxl = 0
      for row_fil in range(row - mid_point + 1, row + mid_point):
        for col_fil in range(col - mid_point + 1, col + mid_point):
          if img[row_fil, col_fil] == 0:
            black_pxl += 1

      # Turn all pixels in noise filter into white if the number of black pixels satisfy the condition given
      if black_pxl >= minblack:
        for row_fil in range(row - mid_point + 1, row + mid_point):
          for col_fil in range(col - mid_point + 1, col + mid_point):
            new_img[row_fil, col_fil] = 255

  # Return the black and white image
  return new_img

"""
This function is designed to remove noise from the image

:param numpy-array img: The image which will be modified
:param integer noise_filsize: The size of the filter
:param integer filstep: How long will the filter move horizontally in each step
:param integer minblack: Maximum number of black pixels in a filter which trigger removal process
:return new_img: Denoised image
"""
def remove_noise(img, noise_filsize, filstep, maxblack):
  # Calculate some border point
  mid_point = (noise_filsize + 1) // 2
  left_most = mid_point - 1
  up_most = mid_point - 1
  right_most = IMG_WIDTH - mid_point + 1
  bottom_most = IMG_HEIGHT - mid_point + 1

  # Copy image
  new_img = np.copy(img)

  # Loop through each pixel
  for row in range(up_most, bottom_most + 1, filstep):
    for col in range(left_most, right_most + 1, filstep):
      # Loop for each pixel in noise filter square
      black_pxl = 0
      for row_fil in range(row - mid_point + 1, row + mid_point):
        for col_fil in range(col - mid_point + 1, col + mid_point):
          if img[row_fil, col_fil] == 0:
            black_pxl += 1

      # Turn all pixels in noise filter into white if the number of black pixels satisfy the condition given
      if black_pxl <= maxblack:
        for row_fil in range(row - mid_point + 1, row + mid_point):
          for col_fil in range(col - mid_point + 1, col + mid_point):
            new_img[row_fil, col_fil] = 255

  # Return the black and white image
  return new_img

"""
This function is designed to sharpen features part of the image

:param numpy-array img: The image which will be modified
:param integer sharpen_filsize: The size of the filter
:param integer filstep: How long will the filter move horizontally in each step
:param integer minblack: Minimum number of black pixels in a filter which trigger the process
:return new_img: Sharpened image
"""
def sharpen(img, sharpen_filsize, filstep, minblack):
  # Calculate some border point
  mid_point = (sharpen_filsize + 1) // 2
  left_most = mid_point - 1
  up_most = mid_point - 1
  right_most = IMG_WIDTH - mid_point + 1
  bottom_most = IMG_HEIGHT - mid_point + 1

  # Copy image
  new_img = np.copy(img)

  # Loop through each pixel
  for row in range(up_most, bottom_most + 1, filstep):
    for col in range(left_most, right_most + 1, filstep):
      # Loop for each pixel in sharpen filter square
      black_pxl = 0
      for row_fil in range(row - mid_point + 1, row + mid_point):
        for col_fil in range(col - mid_point + 1, col + mid_point):
          if img[row_fil, col_fil] == 0:
            black_pxl += 1
            
      # Turn all pixels in noise filter into black if the number of black pixels satisfy the condition given
      if black_pxl >= minblack:
        for row_fil in range(row - mid_point + 1, row + mid_point):
          for col_fil in range(col - mid_point + 1, col + mid_point):
            new_img[row_fil, col_fil] = 0
      
  # Return sharpened image
  return new_img

"""
This function is designed to check whether a pointer is still in the image or not

:param tuple coor: (x, y) coordinate of the pointer
:return bool: True if the pointer inside the image, False otherwise
"""
def is_pos(coor):
  if (coor[0] < 0 or coor[1] < 0) or (coor[0] >= IMG_WIDTH or coor[1] >= IMG_HEIGHT):
    return False
  return True

"""
This function is designed to get all the features from the image

:param numpy-array img: The image which we want to extract its features
:return component: Information about all features.
"""
def get_features(img):
  # Create queue and define some variables needed
  q = []
  for height in range(IMG_HEIGHT):
    for width in range(IMG_WIDTH):
      q.append((height, width))
  done = []
  component = []
  id = 0
  
  # Get all features process using DFS algorithm
  while len(q) >= 1:
    # Remove first element from queue and move to done
    first_el = q[0]
    q.remove(first_el)
    done.append(first_el)
    
    # Define a dictionary to store feature information
    border = {
      "left": first_el[0],
      "right": first_el[0],
      "top": first_el[1],
      "bottom": first_el[1]
    }

    # Run DFS algorithm
    if img[first_el[0], first_el[1]] == 0:
      # Define variables needed
      qn = []
      area = 0

      # Define squares to be checked
      for x_ind in range(- DFS_RADIUS, DFS_RADIUS + 1):
        for y_ind in range(- DFS_RADIUS, DFS_RADIUS + 1):
          # Skip the process if the checked pixel is located on top left or top of the current pixel
          if (x_ind <= 0 and y_ind == 0) or y_ind < 0:
            continue

          cell = (first_el[0] + x_ind, first_el[1] + y_ind)
          if is_pos(cell) and img[cell[0], cell[1]] == 0 and cell not in done:
            qn.append(cell)
            area += 1

            # Get border
            if cell[0] < border["left"]:
              border["left"] = cell[0]
            if cell[0] > border["right"]:
              border["right"] = cell[0]
            if cell[1] < border["top"]:
              border["top"] = cell[1]
            if cell[1] > border["bottom"]:
              border["bottom"] = cell[1]
      
      # Apply DFS to this pixel
      while len(qn) >= 1:
        # Remove first element from queue and move to done
        first_el = qn[0]
        qn.remove(first_el)
        q.remove(first_el)
        done.append(first_el)

        # Define squares to be checked
        for x_ind in range(- DFS_RADIUS, DFS_RADIUS + 1):
          for y_ind in range(- DFS_RADIUS, DFS_RADIUS + 1):
            # Skip the process if the checked pixel is located on top left of current pixel
            if x_ind <= 0 and y_ind <= 0:
              continue

            cell = (first_el[0] + x_ind, first_el[1] + y_ind)
            if is_pos(cell) and img[cell[0], cell[1]] == 0 and cell not in done and cell not in qn:
              qn.append(cell)
              area += 1

              # Get border
              if cell[0] < border["left"]:
                border["left"] = cell[0]
              if cell[0] > border["right"]:
                border["right"] = cell[0]
              if cell[1] < border["top"]:
                border["top"] = cell[1]
              if cell[1] > border["bottom"]:
                border["bottom"] = cell[1]

      # Prepare the information needed that will be stored in the list
      border["area"] = (border["right"] - border["left"]) * (border["bottom"] - border["top"])
      border["mid_x"] = (border["left"] + border["right"]) // 2
      border["mid_y"] = (border["top"] + border["bottom"]) // 2
      border["height"] = border["bottom"] - border["top"]
      border["width"] = border["right"] - border["left"]

      # ---------- Feature selection ----------
      # Apply following rules to decide whether a component is a feature or not
      
      # Rule 1. Total pixels in the component exceed minimum threshold
      if area >= FEATURE_THRES:
        # Rule 2. Component not near the border
        if (
          border['top'] >= BOR_BOUND and
          border['bottom'] < IMG_HEIGHT - BOR_BOUND and
          border['left'] >= BOR_BOUND and
          border['right'] < IMG_WIDTH - BOR_BOUND
        ):
          # Append the information to component array. Each informtion in dictionary form with consists following keys.
          # top: y point of top border
          # bottom: y point of bottom border
          # left: x point of left border
          # right: x point of right border
          # area: the area of framed feature
          # mid_x: axis of center point of the feature
          # mid_y: ordinate of center point of the feature
          # height: height of the feature
          # width: width of the feature
          # id: The id of component
          border['id'] = id
          component.append(border)
          id += 1
  
  # Return feature
  return component

"""
This function is designed to draw border of each feature from an image

:param numpy-array img: The image where we want to draw the border on
:param dictionary border: Contains angle points of each features
:return img: Image with bordered features
"""
def draw_border(img, border):
  # Transpose image
  img = cv2.transpose(img)
  
  # Draw horizontal border
  for hor in [border["top"] - BORDER_PADDING, border["bottom"] + BORDER_PADDING]:
    for pxl in range(border["left"] - BORDER_PADDING, border["right"] + BORDER_PADDING + 1):
      img[hor, pxl, 0] = 255
      img[hor, pxl, 1] = 0
      img[hor, pxl, 2] = 0
  
  # Draw vertical border
  for ver in [border["left"] - BORDER_PADDING, border["right"] + BORDER_PADDING]:
    for pxl in range(border["top"] - BORDER_PADDING, border["bottom"] + BORDER_PADDING + 1):
      img[pxl, ver, 0] = 255
      img[pxl, ver, 1] = 0
      img[pxl, ver, 2] = 0
  
  # Transpose image
  img = cv2.transpose(img)
  
  # Return image
  return img

"""
This function is designed to get all features as an image

:param numpy-array img: The image we want to get the features on
:param dictionary border_col: Array which contains border information of each feature
:return img_col: Array of feature images
"""
def get_features_as_img(img, border_col):
  # Define array to store all feature images
  img_col = []

  # Transpose the image
  img = cv2.transpose(img)
  
  # Loop through each feature
  index = 1
  for border in border_col:
    # Crop the feature and store it as a new image
    feature_img = img[
      border["top"] - BORDER_PADDING: border["bottom"] + 1 + BORDER_PADDING,
      border["left"] - BORDER_PADDING : border["right"] + 1 + BORDER_PADDING
    ]
    feature_img = cv2.transpose(feature_img)

    # ----- Set some variables to make the image squre-shaped -----
    sq_top = 0
    sq_left = 0
    sq_right = 0
    sq_bottom = 0
    diff = border["width"] - border["height"]

    # Case when width < height
    if diff < 0:
      sq_top = (- diff) // 2
      sq_bottom = (- diff) // 2

    # Case when width > height
    elif diff > 0:
      sq_left = diff // 2
      sq_right = diff // 2

    # Add padding to the feature and resize it
    feature_img = cv2.copyMakeBorder(
      feature_img,
      ADD_PADDING + sq_top,
      ADD_PADDING + sq_bottom,
      ADD_PADDING + sq_left,
      ADD_PADDING + sq_right,
      cv2.BORDER_CONSTANT,
      value = 255
    )
    feature_img = cv2.resize(feature_img, (MODEL_HEIGHT, MODEL_WIDTH))

    # Save the image into features folder
    cv2.imwrite('core/features/feature_' + str(index) + '.jpg', feature_img)
    index += 1

    # Rescale the image
    feature_img = feature_img / 255.0

    # Append to the collection
    img_col.append(feature_img)
  
  # Transpose the image
  img = cv2.transpose(img)

  return img_col
