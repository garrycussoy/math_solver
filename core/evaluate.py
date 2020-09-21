"""
This file contains all methods needed to evaluate problem given.
"""

# Import some packages needed
import numbers

"""
Evaluate simple equation (add, substract, multiply, divide, and power).

:param array terms: List of terms
:return result: Result of the calculation
"""
def simple_equation(terms):
  # If there is only 1 term remaining
  if len(terms) == 1:
    return terms[0]
  
  # Calculate expression inside each bracket
  active = False
  counter = 0
  outer_open_bracket_index = 0
  for index in range(len(terms)):
    # If match open bracket
    if terms[index] == '(':
      counter += 1
      if active == False:
        active = True
        outer_open_bracket_index = index
    
    # If match close bracket
    if terms[index] == ')':
      counter -= 1

      # Case when counter equal zero (It means the outer bracket)
      if counter == 0:
        active = False
        terms[outer_open_bracket_index] = simple_equation(terms[outer_open_bracket_index + 1: index])
        return simple_equation(terms[:outer_open_bracket_index + 1] + terms[index + 1:])

  # Do all multiplication and division in the equation
  for index in range(1, len(terms), 2):
    # Searching for the first index which contains a multiplication or a division
    if terms[index] == '$$times$$':
      terms[index + 1] = terms[index - 1] * terms[index + 1]
      return simple_equation(terms[:index - 1] + terms[index + 1:])
    elif terms[index] == '$$division$$':
      terms[index + 1] = terms[index - 1] / terms[index + 1]
      return simple_equation(terms[:index - 1] + terms[index + 1:])
  
  # Evaluate remaining equation from left to right (it will be addition and substraction only)
  if terms[1] == '+':
    terms[2] = terms[0] + terms[2]
    return simple_equation(terms[2:])
  elif terms[1] == '-':
    terms[2] = terms[0] - terms[2]
    return simple_equation(terms[2:])
  
"""
Classifier of which method will be used for given terms and topic

:param array terms: List of terms
:param string topic: The topic of the problem
:return: Result of the calculation
"""
def evaluate(terms, topic):
  # Classify the calculation by its topic
  if topic == "simple_equation":
    return simple_equation(terms)
