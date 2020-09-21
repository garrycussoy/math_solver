"""
This file contains display methods for each topic given.
"""

"""
Display question and answer of problem which fall into simple question topic.

:param array terms: List of terms
:param integer answer: The answer of the question
"""
def display_simple_equation(terms, answer):
  # Replace some operation with appropiate symbol
  for index in range(len(terms)):
    if terms[index] == "$$times$$":
      terms[index] = "x"
  
  # Get the question in a string format
  question = " ".join(list(map(str, terms)))

  # Display the question and answer
  print("=========================================================================")
  print("Question : " + question)
  print("Answer   : " + str(answer))
  print("=========================================================================")

"""
Classifier of which method will be used for given terms and topic

:param array terms: List of terms
:param integer answer: The answer of the problem
:param string topic: The topic of the problem
"""
def display_qna(terms, answer, topic):
  # Classify by its topic
  if topic == "simple_equation":
    display_simple_equation(terms, answer)
