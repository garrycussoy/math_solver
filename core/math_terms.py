"""
This file contains functions needed to turn all features into a comprehensive mathematical form.
"""

# Import variables needed from other modules
from core.math_symbol import math_symbol

"""
This function is designed to get position order of each feature.

:param dictionary features: List of the features
:return features: List of ordered features
"""
def arrange_position(features):
  # Reorder the list according to their horizontal position
  repeat = True
  while repeat:
    repeat = False
    for index in range(len(features) - 1):
      if features[index + 1]["mid_y"] < features[index]["mid_y"]:
        dummy = features[index]
        features[index] = features[index + 1]
        features[index + 1] = dummy
        repeat = True
  
  # Return ordered features list
  return features

"""
This function is designed to classify what function will be executed for the given topic.

:param dictionary features: List of the features
:param string topic: Topic of the problem
:return math_terms: List of all mathematics terms converted from the features
"""
def get_math_terms(features, topic):
  # Classify the execution by its topic
  if topic == "simple_equation":
    return get_term_simple_equation(features)

"""
Get mathematics terms of simple equation problem.

:param dictionary features: List of the features
:return math_terms: List of all mathematics terms converted from the features
"""
def get_term_simple_equation(features):
  # Define some variables needed
  math_terms = []
  ordinate = [] # To store vertical position of dash symbol
  number = ''
  
  # ---------- First Step ----------
  # Get all numbers and symbols involved by looping through each feature
  numb_features = len(features)
  for index in range(numb_features):
    # Case when the feature is a number
    if features[index]["symbol_id"] <= 9:
      number += features[index]["symbol"]
    
    # Case when the feature is not a number
    else:
      if len(number) > 0:
        math_terms.append(int(number))
        ordinate.append(None)
        number = ''

      # Special case when the symbol is dash
      if features[index]["symbol"] == '-':
        ordinate.append(features[index]["mid_x"])
      else:
        ordinate.append(None)
      math_terms.append(features[index]["symbol"])
    
    # Case for last element and it is a number
    if index == numb_features - 1 and len(number) > 0:
      math_terms.append(int(number))
      ordinate.append(None)
  
  # ---------- Second Step ----------
  # Detect equal sign
  terms_iter = math_terms.copy()
  math_terms = []
  index = 0
  while index < len(terms_iter):
    # Case when there is two adjacent dash symbols and located up and down in the image
    if index != len(terms_iter) - 1:
      if (
        terms_iter[index] == '-' and
        terms_iter[index + 1] == '-' and
        abs(ordinate[index] - ordinate[index + 1]) >= 5
      ):
        index += 2
        continue
    
    # Other cases
    math_terms.append(terms_iter[index])
    index += 1
  
  # ---------- Third Step ----------
  # Detect negative integer
  terms_iter = math_terms.copy()
  math_terms = []
  index = 0
  while index < len(terms_iter):
    # Case first term is a dash sign followed by a number
    if index == 0 and terms_iter[index] == '-' and isinstance(terms_iter[index + 1], int) and len(terms_iter) > 1:
      math_terms.append((-1) * terms_iter[index + 1])
      index += 2
      continue
    
    # Case when a dash symbol is located after non-number symbol and before a number
    if (
      index > 0 and
      index < len(terms_iter) - 1 and
      terms_iter[index] == '-' and
      (terms_iter[index - 1] == '+' or terms_iter[index - 1] == '-' or terms_iter[index - 1] == '$$times$$' or terms_iter[index - 1] == '(') and
      isinstance(terms_iter[index + 1], int)
    ):
      math_terms.append((-1) * terms_iter[index + 1])
      index += 2
      continue
    
    # Other cases
    math_terms.append(terms_iter[index])
    index += 1

  # Return the terms
  return math_terms
